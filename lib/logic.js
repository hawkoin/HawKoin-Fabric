/**
 * New script file
 */
'use strict';

/**
 * Track the trade of a commodity from one participant to another
 * @param {org.hawkoin.network.TransferFunds} trade - the trade to be processed
 * @transaction
 */
async function transferFunds(trade) {
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
    else if(trade.fromUser.getFullyQualifiedType() === 'org.hawkoin.network.Student') {
        if (trade.toUser.getFullyQualifiedType() === 'org.hawkoin.network.Student' ||
            trade.toUser.getFullyQualifiedType() === 'org.hawkoin.network.Faculty' ||
            trade.toUser.getFullyQualifiedType() === 'org.hawkoin.network.Administrator'
        ) {
            // Throw Error, rolls back transaction
            throw new Error('Transaction Failed. Students cannot trade with Students, Faculty, or Administrators.');
        }
    }
    // Faculty cannot transact with Students, Faculty, or Administrators
    else if(trade.fromUser.getFullyQualifiedType() === 'org.hawkoin.network.Faculty') {
        if (trade.toUser.getFullyQualifiedType() === 'org.hawkoin.network.Student' ||
            trade.toUser.getFullyQualifiedType() === 'org.hawkoin.network.Faculty' ||
            trade.toUser.getFullyQualifiedType() === 'org.hawkoin.network.Administrator'
        ) {
            // Throw Error, rolls back transaction
            throw new Error('Transaction Failed. Faculty cannot trade with Students, Faculty, or Administrators.');
        }
    }
    // Administrators cannot transact with Students, Faculty, or Administrators
    else if(trade.fromUser.getFullyQualifiedType() === 'org.hawkoin.network.Administrator') {
        if (trade.toUser.getFullyQualifiedType() === 'org.hawkoin.network.Student' ||
            trade.toUser.getFullyQualifiedType() === 'org.hawkoin.network.Faculty' ||
            trade.toUser.getFullyQualifiedType() === 'org.hawkoin.network.Administrator'
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