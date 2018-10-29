/**
 * New script file
 */
'use strict';
/**
 * Track the trade of a commodity from one trader to another
 * @param {org.hawkoin.network.TransferFunds} trade - the trade to be processed
 * @transaction
 */
async function transferFunds(trade) {
    if(trade.fromUser.getFullyQualifiedType() === 'org.hawkoin.network.Student' &&
    trade.toUser.getFullyQualifiedType() === 'org.hawkoin.network.Student' ) {
        throw new Error('Transaction Failed. Students cannot trade with other Students.');
    }

    else if (trade.fromUser.balance >= trade.amount) {

        trade.fromUser.balance -= trade.amount;
        trade.toUser.balance += trade.amount;

        await getParticipantRegistry(trade.fromUser.getFullyQualifiedType()).then(function(partRegistry) {
            return partRegistry.update(trade.fromUser);
        });

        await getParticipantRegistry(trade.toUser.getFullyQualifiedType()).then(function(partRegistry) {
            return partRegistry.update(trade.toUser);
        });

        var options = {
            url: 'https://api.sendgrid.com/v3/mail/send',
            headers: {
                'Authorization': 'Bearer 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',
                'Access-Control-Allow-Origin': 'http://localhost:8080',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, PATCH, DELETE',
                'Content-Type': 'application/json'
            },
            data: {
                'personalizations': [{ 'to': [ { 'email': 'maddessi1@gmail.com' }]}],
                'from': {'email': 'sendeexampexample@example.com'}, 'subject': 'Hello, World!', 'content': [{'type': 'text/plain', 'value': 'Heya!'}]
            }
        };
        //alert(options);
        console.log(options);
        console.log(request.post(options));

    }
    else {
        throw new Error('Transaction failed. Insufficient funds.');
    }
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