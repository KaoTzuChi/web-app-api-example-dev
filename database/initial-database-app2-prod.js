/* 
==============================================================================
load("data/db/initial-database-app2-prod.js")
==============================================================================
*/

var conn=null;
var db=null;
var dbadmin=null;

try {
    conn = new Mongo("127.0.0.1:27017");
    print ('<< 1. mongo service: ok >>');
    try {
        dbadmin = conn.getDB("admin");
        dbadmin.auth( "root", "311076" );
        db = dbadmin.getSiblingDB('mydatabase');
        print ('<< 2. connect to mydatabase: ok >>');

        // create a new user for later app accessing.
        try {   
            db.createUser({
                "user" : "myuser",
                "pwd" : "myuserspwd",
                "roles" : [
                    { "db" : "mydatabase", "role": "readWrite" },
                    { "db" : "mydatabase", "role": "dbAdmin" },
                    { "db" : "mydatabase", "role": "dbOwner" },
                    { "db" : "mydatabase", "role": "userAdmin" }
                ]
            });
            print ('<< 3. createuser: ok >>');
        } catch (e) {
            print ('<< 3. createuser: FAIL >>'+e);
        }

        // initialize mycollectionone, in mydatabase, by user root.
        try {
            db.createCollection("mycollectionone", { autoIndexId: true } );
            db.mycollectionone.remove({});
            db.mycollectionone.insertMany([
            { "field11": "valueof-doc1-field1", "field12":{"item1":"valueof-doc1-field2-item1", "item2":"valueof-doc1-field2-item2"}, "field13": new Date("2011-01-01 01:01:01+01:00"), "field14":1.01, "field15":["a","b","c","d"] },
            { "field11": "valueof-doc2-field1", "field12":{"item1":"valueof-doc2-field2-item1", "item2":"valueof-doc2-field2-item2"}, "field13": new Date("2012-02-02 02:02:02+02:00"), "field14":2.02, "field15":["a","b"] },
            { "field11": "valueof-doc3-field1", "field12":{"item1":"valueof-doc3-field2-item1", "item2":"valueof-doc3-field2-item2"}, "field13": new Date("2013-03-03 03:03:03+03:00"), "field14":3.03, "field15":["c","d"] },
            { "field11": "valueof-doc4-field1", "field12":{"item1":"valueof-doc4-field2-item1", "item2":"valueof-doc4-field2-item2"}, "field13": new Date("2014-04-04 04:04:04+04:00"), "field14":4.04, "field15":["b","c","d"] },
            { "field11": "valueof-doc5-field1", "field12":{"item1":"valueof-doc5-field2-item1", "item2":"valueof-doc5-field2-item2"}, "field13": new Date("2015-05-05 05:05:05+05:00"), "field14":5.05, "field15":["a","d"] },
            { "field11": "valueof-doc6-field1", "field12":{"item1":"valueof-doc6-field2-item1", "item2":"valueof-doc6-field2-item2"}, "field13": new Date("2016-06-06 06:06:06+06:00"), "field14":6.06, "field15":["a","f","e","d"] },
            { "field11": "valueof-doc7-field1", "field12":{"item1":"valueof-doc7-field2-item1", "item2":"valueof-doc7-field2-item2"}, "field13": new Date("2017-07-07 07:07:07+07:00"), "field14":7.07, "field15":["a","b","c","f"] },
            { "field11": "valueof-doc8-field1", "field12":{"item1":"valueof-doc8-field2-item1", "item2":"valueof-doc8-field2-item2"}, "field13": new Date("2018-08-08 08:08:08+08:00"), "field14":8.08, "field15":["a","e"] },
            { "field11": "valueof-doc9-field1", "field12":{"item1":"valueof-doc9-field2-item1", "item2":"valueof-doc9-field2-item2"}, "field13": new Date("2019-09-09 09:09:09+09:00"), "field14":9.09, "field15":["d","f"] }
            ]);
            print ('<< initialize mycollectionone: ok >>');
        } catch (e) {print ('<< initialize mycollectionone: FAIL >>'+e);}

        // initialize mycollectiontwo, in mydatabase, by user root.
        try {
            db.createCollection("mycollectiontwo", { autoIndexId: true } );
            db.mycollectiontwo.remove({});
            db.mycollectiontwo.insertMany([
            { "field21": "valueof-doc1-field1", "field22":{"item1":"valueof-doc1-field2-item1", "item2":"valueof-doc1-field2-item2"}, "field23": new Date("2011-01-01 01:01:01+01:00"), "field24":1.01, "field25":["a","c","d"] },
            { "field21": "valueof-doc2-field1", "field22":{"item1":"valueof-doc2-field2-item1", "item2":"valueof-doc2-field2-item2"}, "field23": new Date("2012-02-02 02:02:02+02:00"), "field24":2.02, "field25":["b","c","d"] },
            { "field21": "valueof-doc3-field1", "field22":{"item1":"valueof-doc3-field2-item1", "item2":"valueof-doc3-field2-item2"}, "field23": new Date("2013-03-03 03:03:03+03:00"), "field24":3.03, "field25":["a","b","d"] },
            { "field21": "valueof-doc4-field1", "field22":{"item1":"valueof-doc4-field2-item1", "item2":"valueof-doc4-field2-item2"}, "field23": new Date("2014-04-04 04:04:04+04:00"), "field24":4.04, "field25":["a","b","c"] },
            { "field21": "valueof-doc5-field1", "field22":{"item1":"valueof-doc5-field2-item1", "item2":"valueof-doc5-field2-item2"}, "field23": new Date("2015-05-05 05:05:05+05:00"), "field24":5.05, "field25":["a","b"] },
            { "field21": "valueof-doc6-field1", "field22":{"item1":"valueof-doc6-field2-item1", "item2":"valueof-doc6-field2-item2"}, "field23": new Date("2016-06-06 06:06:06+06:00"), "field24":6.06, "field25":["b","c"] },
            { "field21": "valueof-doc7-field1", "field22":{"item1":"valueof-doc7-field2-item1", "item2":"valueof-doc7-field2-item2"}, "field23": new Date("2017-07-07 07:07:07+07:00"), "field24":7.07, "field25":["c","d"] },
            { "field21": "valueof-doc8-field1", "field22":{"item1":"valueof-doc8-field2-item1", "item2":"valueof-doc8-field2-item2"}, "field23": new Date("2018-08-08 08:08:08+08:00"), "field24":8.08, "field25":["a","f","c","d"] },
            { "field21": "valueof-doc9-field1", "field22":{"item1":"valueof-doc9-field2-item1", "item2":"valueof-doc9-field2-item2"}, "field23": new Date("2019-09-09 09:09:09+09:00"), "field24":9.09, "field25":["a","e","d","d"] }
            ]);
            print ('<< initialize mycollectiontwo: ok >>');
        } catch (e) {print ('<< initialize mycollectiontwo: FAIL >>'+e);}

        // initialize mycollectionthree, in mydatabase, by user root.
        try {
            db.createCollection("mycollectionthree", { autoIndexId: true } );
            db.mycollectionthree.remove({});
            db.mycollectionthree.insertMany([
            { "field31": "Sunday", "field32":100, "field33": 9, "field34":1.01, "field35":["a","c","d"] },
            { "field31": "Monday", "field32":150, "field33": 8, "field34":2.02, "field35":["b","c","d"] },
            { "field31": "Tuesday", "field32":200, "field33": 1, "field34":3.03, "field35":["a","b","d"] },
            { "field31": "Wednesday", "field32":220, "field33": 5, "field34":4.04, "field35":["a","b","c"] },
            { "field31": "Thursday", "field32":300, "field33": 3, "field34":5.05, "field35":["a","b"] },
            { "field31": "Sunday", "field32":360, "field33": 4, "field34":6.06, "field35":["b","c"] },
            { "field31": "Friday", "field32":400, "field33": 2, "field34":7.07, "field35":["c","d"] },
            { "field31": "Monday", "field32": 20, "field33": 6, "field34":8.08, "field35":["a","f","c","d"] },
            { "field31": "Thursday", "field32":480, "field33": 7, "field34":9.09, "field35":["a","e","d","d"] }
            ]);
            print ('<< initialize mycollectionthree: ok >>');
        } catch (e) {print ('<< initialize mycollectionthree: FAIL >>'+e);}

        // initialize productcollection, in mydatabase, by user root.
        try {
            db.createCollection("productcollection", { autoIndexId: true } );
            db.productcollection.remove({});
            db.productcollection.insertMany([
            { "title": "product one", "brief": "brief 1", "price":100, "contact": "+886-2-1111-1111", "location": "location one", "lastupdate":new Date("2011-01-01 01:01:01+01:00"), "tags":["a","c","d"] },
            { "title": "product two", "brief": "brief 2", "price":150, "contact": "+886-2-2222-2222", "location": "location two", "lastupdate":new Date("2011-01-01 01:01:01+01:00"), "tags":["b","c","d"] },
            { "title": "product three", "brief": "brief 3", "price":200, "contact": "+886-2-3333-3333", "location": "location three", "lastupdate":new Date("2011-01-01 01:01:01+01:00"), "tags":["a","b","d"] },
            { "title": "product four", "brief": "brief 4", "price":220, "contact": "+886-2-4444-4444", "location": "location four", "lastupdate":new Date("2011-01-01 01:01:01+01:00"), "tags":["a","b","c"] },
            { "title": "product five", "brief": "brief 5", "price":300, "contact": "+886-2-5555-5555", "location": "location five", "lastupdate":new Date("2011-01-01 01:01:01+01:00"), "tags":["a","b"] },
            { "title": "product six", "brief": "brief 6", "price":360, "contact": "+886-2-6666-6666", "location": "location six", "lastupdate":new Date("2011-01-01 01:01:01+01:00"), "tags":["b","c"] },
            { "title": "product seven", "brief": "brief 7", "price":400, "contact": "+886-2-7777-7777", "location": "location seven", "lastupdate":new Date("2011-01-01 01:01:01+01:00"), "tags":["c","d"] },
            { "title": "product eight", "brief": "brief 8", "price": 20, "contact": "+886-2-8888-8888", "location": "location eight", "lastupdate":new Date("2011-01-01 01:01:01+01:00"), "tags":["a","f","c","d"] },
            { "title": "product nine", "brief": "brief 9", "price":480, "contact": "+886-2-9999-9999", "location": "location nine", "lastupdate":new Date("2011-01-01 01:01:01+01:00"), "tags":["a","e","d","d"] }
            ]);
            print ('<< initialize productcollection: ok >>');
        } catch (e) {print ('<< initialize productcollection: FAIL >>'+e);}

        // initialize shoppingcartcollection, in mydatabase, by user root.
        try {
            db.createCollection("shoppingcartcollection", { autoIndexId: true } );
            db.shoppingcartcollection.remove({});
            db.shoppingcartcollection.insertMany([
            { "productid": "5eb7d4b2338af773dd96f6fc", "productname": "product aaa", "orderid": "None", "memberid": 'user1', "price":100, "discount": 0.05, "count":1,  "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "productid": "5eb7d4b2338af773dd96f6fc", "productname": "product bbb", "orderid": "None", "memberid": 'user3', "price":150, "discount": 0.15, "count":2,  "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "productid": "5eb7d4b2338af773dd96f6fc", "productname": "product ccc", "orderid": "None", "memberid": 'user2', "price":200, "discount": 0.20, "count":3,  "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "productid": "5eb7d4b2338af773dd96f6fc", "productname": "product ddd", "orderid": "None", "memberid": 'user1', "price":220, "discount": 0.25, "count":1,  "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "productid": "5eb7d4b2338af773dd96f6fc", "productname": "product eee", "orderid": "None", "memberid": 'user3', "price":300, "discount": 0.30, "count":2,  "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "productid": "5eb7d4b2338af773dd96f6fc", "productname": "product fff", "orderid": "None", "memberid": 'user1', "price":360, "discount": 0.35, "count":3,  "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "productid": "5eb7d4b2338af773dd96f6fc", "productname": "product ggg", "orderid": "None", "memberid": 'user2', "price":400, "discount": 0.40, "count":1,  "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "productid": "5eb7d4b2338af773dd96f6fc", "productname": "product hhh", "orderid": "None", "memberid": 'user1', "price": 20, "discount": 0.45, "count":2,  "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "productid": "5eb7d4b2338af773dd96f6fc", "productname": "product iii", "orderid": "None", "memberid": 'user2', "price":480, "discount": 0.50, "count":3,  "lastupdate":new Date("2011-01-01 01:01:01+01:00") }
            ]);
            print ('<< initialize shoppingcartcollection: ok >>');
        } catch (e) {print ('<< initialize shoppingcartcollection: FAIL >>'+e);}

        // initialize ordercollection, in mydatabase, by user root.
        try {
            db.createCollection("ordercollection", { autoIndexId: true } );
            db.ordercollection.remove({});
            db.ordercollection.insertMany([
            { "payment": "payment1", "status": 0, "memberid": 'user1', "totalprice":100, "totaldiscount": 100, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "payment": "payment2", "status": 1, "memberid": 'user1', "totalprice":150, "totaldiscount": 100, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "payment": "payment3", "status": 2, "memberid": 'user2', "totalprice":200, "totaldiscount": 100, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "payment": "payment1", "status": 3, "memberid": 'user3', "totalprice":220, "totaldiscount": 100, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "payment": "payment2", "status": 0, "memberid": 'user1', "totalprice":300, "totaldiscount": 100, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "payment": "payment3", "status": 1, "memberid": 'user1', "totalprice":360, "totaldiscount": 100, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "payment": "payment1", "status": 2, "memberid": 'user2', "totalprice":400, "totaldiscount": 100, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "payment": "payment2", "status": 3, "memberid": 'user3', "totalprice": 20, "totaldiscount": 100, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "payment": "payment3", "status": 4, "memberid": 'user3', "totalprice":480, "totaldiscount": 100, "lastupdate":new Date("2011-01-01 01:01:01+01:00") }
            ]);
            print ('<< initialize ordercollection: ok >>');
        } catch (e) {print ('<< initialize ordercollection: FAIL >>'+e);}

        // initialize callbackcollection, in mydatabase, by user root.
        try {
            db.createCollection("callbackcollection", { autoIndexId: true } );
            db.callbackcollection.remove({});
            db.callbackcollection.insertMany([
            { "sender": "oauth", "data": {"status":"valueofitem1", "data":"valueofitem2"}, "statuscode":100, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "sender": "oauth", "data": {"status":"valueofitem1", "data":"valueofitem2"}, "statuscode":150, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "sender": "oauth", "data": {"status":"valueofitem1", "data":"valueofitem2"}, "statuscode":200, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "sender": "oauth", "data": {"status":"valueofitem1", "data":"valueofitem2"}, "statuscode":220, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "sender": "oauth", "data": {"status":"valueofitem1", "data":"valueofitem2"}, "statuscode":300, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "sender": "oauth", "data": {"status":"valueofitem1", "data":"valueofitem2"}, "statuscode":360, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "sender": "oauth", "data": {"status":"valueofitem1", "data":"valueofitem2"}, "statuscode":400, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "sender": "oauth", "data": {"status":"valueofitem1", "data":"valueofitem2"}, "statuscode": 20, "lastupdate":new Date("2011-01-01 01:01:01+01:00") },
            { "sender": "oauth", "data": {"status":"valueofitem1", "data":"valueofitem2"}, "statuscode":480, "lastupdate":new Date("2011-01-01 01:01:01+01:00") }
            ]);
            print ('<< initialize callbackcollection: ok >>');
        } catch (e) {print ('<< initialize callbackcollection: FAIL >>'+e);}

    } catch (e) {
        print ('<< 2. connect to mydatabase: FAIL >>'+e);
    }
} catch (e) {
    print ('<< 1. mongo service: FAIL >>'+e);
}



