/**
 * Smart contract logic
 */
'use strict';

/* DO NOT REMOVE THIS COMMENT BLOCK. NEEDED FOR UNIT TEST COMPILATION */
/* global getAssetRegistry getFactory emit request */
/* global getAssetRegistry getFactory emit query */

/**
 * Track the trade of a commodity from one participant to another
 * @param {string} fromUserID - wallet to authorize
 * @param {string} authToken - google oauth token for authorization
 */
async function verifyOAuth(fromUserID, authToken) {
    try {
        var OAuthResponse = await (request.get('https://www.googleapis.com/oauth2/v2/userinfo', {
            'auth': {
                'bearer': authToken
            }
        }));
        var googleID = JSON.parse(OAuthResponse).email;

        if (fromUserID === googleID) {
            return true;
        }

    } catch(error) {
        return false;
    }
    return false;
}
/**
 * Track the trade of a commodity from one participant to another
 * @param {org.hawkoin.network.TransferFunds} trade - the trade to be processed
 * @transaction
 */
async function transferFunds(trade) {

    var txnAuthenticated = false;

    var demoMode = await getAssetRegistry('org.hawkoin.network.DemoMode')
        .then(function (demoModeRegistry) {
            return demoModeRegistry.exists('activated');
        });

    if (demoMode) {
        txnAuthenticated = true;
    }
    else {
        txnAuthenticated = await verifyOAuth(trade.fromUser.id, trade.authToken);
    }

    if (!txnAuthenticated) {
        throw new Error('Transaction failed. Authentication invalid.');
    }

    var fromType = trade.fromUser.getFullyQualifiedType();
    var toType = trade.toUser.getFullyQualifiedType();
    // Cannot transact if not sufficient funds
    if(trade.fromUser.balance < trade.amount) {
        throw new Error('Transaction failed. Insufficient funds.');
    }
    // Check if participants are both active
    else if(trade.fromUser.isActive === false) {
        throw new Error('Transaction failed. The sending account is inactive.');
    }
    else if(trade.toUser.isActive === false) {
        throw new Error('Transaction failed. The receiving account is inactive.');
    }
    // Students cannot transact with Students, Faculty, or Administrators
    else if(fromType === 'org.hawkoin.network.Student') {
        if (toType === 'org.hawkoin.network.Student' ||
            toType === 'org.hawkoin.network.Faculty' ||
            toType === 'org.hawkoin.network.Administrator'
        ) {
            // Throw Error, rolls back transaction
            throw new Error('Transaction Failed. Students cannot trade with Students, Faculty, or Administrators.');
        }
    }
    // Faculty cannot transact with Students, Faculty, or Administrators
    else if(fromType === 'org.hawkoin.network.Faculty') {
        if (toType === 'org.hawkoin.network.Student' ||
            toType === 'org.hawkoin.network.Faculty' ||
            toType === 'org.hawkoin.network.Administrator'
        ) {
            // Throw Error, rolls back transaction
            throw new Error('Transaction Failed. Faculty cannot trade with Students, Faculty, or Administrators.');
        }
    }
    // Administrators cannot transact with Students, Faculty, or Administrators
    else if(fromType === 'org.hawkoin.network.Administrator') {
        if (toType === 'org.hawkoin.network.Student' ||
            toType === 'org.hawkoin.network.Faculty' ||
            toType === 'org.hawkoin.network.Administrator'
        ) {
            // Throw Error, rolls back transaction
            throw new Error('Transaction Failed. Administrator cannot trade with Students, Faculty, or Administrators.');
        }
    }
    // If transaction breaks a threshold
    var rb = trade.fromUser.balance - trade.amount;
    if(trade.amount > trade.fromUser.txnThreshold) {
        const highTxn = getFactory().newEvent('org.hawkoin.network', 'TransactionThreshBreach');
        highTxn.info = trade.fromUser.contactInfo;
        emit(highTxn);
    }
    else if(rb < trade.fromUser.lowBalThreshold) {
        const lowBal = getFactory().newEvent('org.hawkoin.network', 'LowBalanceAlert');
        lowBal.info = trade.fromUser.contactInfo;
        emit(lowBal);
    }

    // Velocity Check
    let earlier = new Date();
    const velocityThresh = 5;
    earlier.setMinutes(earlier.getMinutes() - velocityThresh);
    var userString = 'resource:' + fromType + '#' + trade.fromUser.id;
    let results = await query('velocityCheck',{stamp:earlier, user:userString});
    // If we have 3 transactions within 5 minutes - there's maybe a problem
    if(results.length >= 2) {
        const velocityWarning = getFactory().newEvent('org.hawkoin.network', 'VelocityWarning');
        velocityWarning.info = trade.fromUser.contactInfo;
        emit(velocityWarning);
    }

    // No Errors, make the trade
    trade.fromUser.balance -= trade.amount;
    trade.toUser.balance += trade.amount;
    await getParticipantRegistry(trade.fromUser.getFullyQualifiedType()).then(function(partRegistry) {
        return partRegistry.update(trade.fromUser);
    });
    await getParticipantRegistry(trade.toUser.getFullyQualifiedType()).then(function(partRegistry) {
        return partRegistry.update(trade.toUser);
    });
    // emit an event with the remaining balance
    const remBal = getFactory().newEvent('org.hawkoin.network', 'RemainingBalance');
    remBal.remainingBal = rb;
    emit(remBal);
}

/**
 * Track the deposit or creation of funds into an account
 * @param {org.hawkoin.network.CreateFunds} tx - the addition to be processed
 * @transaction
 */
async function CreateFunds(tx) {
    tx.toUser.balance += tx.amount;
    await getParticipantRegistry(tx.toUser.getFullyQualifiedType()).then(function(partRegistry) {
        return partRegistry.update(tx.toUser);
    });
}


/**
 * Track the deletion of funds from an account
 * @param {org.hawkoin.network.DeleteFunds} tx - the transaction to be processed
 * @transaction
 */
async function deleteFunds(tx) {

    if (tx.fromUser.balance >= tx.amount) {
        tx.fromUser.balance -= tx.amount;
        await getParticipantRegistry(tx.fromUser.getFullyQualifiedType()).then(function(partRegistry) {
            return partRegistry.update(tx.fromUser);
        });
    }
    else {
        tx.fromUser.balance = 0;
        await getParticipantRegistry(tx.fromUser.getFullyQualifiedType()).then(function(partRegistry) {
            return partRegistry.update(tx.fromUser);
        });
    }
}

/**
 * Track the change of the minimum balance threshold for a user
 * @param {org.hawkoin.network.ChangeLowBalAlert} tx - the transaction to be processed
 * @transaction
 */
async function changeLowBalAlert(tx) {
    tx.user.lowBalThreshold = tx.thresh;
    await getParticipantRegistry(tx.user.getFullyQualifiedType()).then(function(partRegistry) {
        return partRegistry.update(tx.user);
    });
}

/**
 * Track the change of the maximum transaction threshold for a user
 * @param {org.hawkoin.network.ChangeTxnBreach} tx - the transaction to be processed
 * @transaction
 */
async function changeTxnBreach(tx) {
    tx.user.txnThreshold = tx.thresh;
    await getParticipantRegistry(tx.user.getFullyQualifiedType()).then(function(partRegistry) {
        return partRegistry.update(tx.user);
    });
}

/**
 * Track the deletion of funds from an account
 * @param {org.hawkoin.network.ChangeContactInfo} tx - the transaction to be processed
 * @transaction
 */
async function changeContactInfo(tx) {

    // Only update if transaction field is filled in
    if(tx.newFirst !== '') {
        tx.user.contactInfo.firstName = tx.newFirst;
    }
    if(tx.newLast !== '') {
        tx.user.contactInfo.lastName = tx.newLast;
    }
    if(tx.newEmail !== '') {
        tx.user.contactInfo.email = tx.newEmail;
    }
    if(tx.newAdd !== '') {
        tx.user.contactInfo.address = tx.newAdd;
    }
    if(tx.newCity !== '') {
        tx.user.contactInfo.city = tx.newCity;
    }
    if(tx.newState !== '') {
        tx.user.contactInfo.state = tx.newState;
    }
    if(tx.newZip !== '') {
        tx.user.contactInfo.zip = tx.newZip;
    }

    await getParticipantRegistry(tx.user.getFullyQualifiedType()).then(function(partRegistry) {
        return partRegistry.update(tx.user);
    });
}