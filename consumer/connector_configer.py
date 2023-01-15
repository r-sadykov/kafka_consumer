from confluent_kafka import Consumer, OFFSET_BEGINNING
import consumer.connector_globals as globals
from consumer.connector_http import putToDb
from consumer.connector_logger import print_sourceInfo
from consumer.connector_methods import *


class KafkaConsumer:
    def __init__(self, config_parser, isReset) -> None:
        self.topic = config_parser['topics']['topic']
        self.isReset = isReset
        # Create Consumer instance
        self.config = self.setConfig(config_parser)
        self.consumer = Consumer(self.config)

    def setConfig(self, config_parser):
        config = {}
        config = dict(config_parser['default'])
        config.update(config_parser['consumer'])
        return config

     # Set up a callback to handle the '--reset' flag.
    def reset_offset(self, consumer, partitions):
        if self.isReset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topic
    def subscribe(self):
        self.consumer.subscribe([self.topic], on_assign=self.reset_offset)
        print(f"Connecting to TOPIC {self.topic}")

    # Poll for new messages from Kafka and print them.
    def consume(self):
        consumedCounter = 0
        clientLogCounter = 0
        nboLogCounter = 0
        nboResponseLogCounter = 0
        othersCounter = 0
        errorCounter = 0
        users = []
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if globals.users is not None:
                    users = globals.users
                else:
                    users = globals.prev_users
                if msg is None:
                    # Initial message consumption may take up to
                    # `session.timeout.ms` for the consumer group to
                    # rebalance and start consuming
                    print("Waiting...")
                elif msg.error():
                    print("ERROR: %s".format(msg.error()))
                else:
                    # Extract the (optional) key and value, and print.
                    # print("Consumed event from topic {topic}: key = {key} value = {value}".format(
                    #    topic=msg.topic(), key=msg.key(), value=msg.value()))
                    try:
                        log = value_toKafkaObject(msg.value().decode('utf-8'))
                        globals.stats.setUsersCounter(len(users))
                        if log is not None:
                            globals.stats.raiseConsumerCounter
                            if isClientLog(log):
                                clientLog = getClientLog(log)
                                if clientLog is not None:
                                    if isLoginExist(clientLog):
                                        clientLog = filterClientLogByUser(
                                            clientLog, users)
                                        clientLog = filterClientLogByChannel(
                                            clientLog, globals.config_parser['filters']['channels'])
                                        clientLog = filterClientLogByUrl(
                                            clientLog, globals.config_parser['filters']['client_log_url'])
                                        clientLog = filterClientLogBySize(
                                            clientLog, 1)
                                        clientLog = filterClientLogByStatus(
                                            clientLog, 'success')
                                        clientLog = filterClientLogByGuid(
                                            clientLog)
                                        if clientLog is not None:
                                            globals.stats.raiseClientLogCounter
                                            clientDb = ClientLogDB(client_guid=clientLog.body.data.clients[0].base.guid,
                                                                   response_status=clientLog.body.status,
                                                                   body_actual_timestamp=clientLog.body.actual_timestamp,
                                                                   trace_id=log.context_map.trace_id,
                                                                   login=clientLog.login,
                                                                   categories=encapsulate(
                                                                       clientLog.body.data.clients[0].base.categories),
                                                                   created_at=log.created_at,
                                                                   clients_quantity=len(
                                                                       clientLog.body.data.clients)
                                                                   )
                                            try:
                                                url = globals.config_parser['connections']['post_logs_url']
                                                url = url[1:-1]
                                                toDB = json.dumps(
                                                    clientLogDB_toDict(clientDb), ensure_ascii=False)
                                                if globals.config_parser.getboolean('filters', 'isFigured'):
                                                    toDB = toDB.replace(
                                                        '[', '{').replace(']', '}')
                                                putted = putToDb(
                                                    url, type(clientDb).__name__, clientDb.login, toDB)
                                                if putted == False:
                                                    print_sourceInfo(
                                                        "Failed in DB load", clientDb, clientLog.login, "-p")
                                            except Exception as e:
                                                print_errorInfo(e)
                                        else:
                                            globals.stats.raiseOthersCounter
                                    else:
                                        globals.stats.raiseOthersCounter
                                else:
                                    globals.stats.raiseOthersCounter
                            elif isNboLog(log):
                                nboLog = getNboLog(log)
                                if nboLog is not None:
                                    if isLoginExist(nboLog):
                                        nboLog = filterNboLogByUser(
                                            nboLog, users)
                                        nboLog = filterNboLogByChannel(
                                            nboLog, globals.config_parser['filters']['channels'])
                                        nboLog = filterNboLogByGuid(nboLog)
                                        nboLog = filterNboLogByOfferId(nboLog)
                                        if nboLog is not None:
                                            globals.stats.raiseNboLogCounter
                                            nboDb = NboLogDB(trace_id=log.context_map.trace_id,
                                                             gpb_guid=nboLog.gpb_guid,
                                                             user_login=nboLog.user_login,
                                                             created_at=log.created_at,
                                                             contact_id=nboLog.contact_id,
                                                             offer_id=nboLog.offer_id,
                                                             product_code=nboLog.product_code,
                                                             product_name=nboLog.product_name,
                                                             priority=nboLog.priority,
                                                             date_time=nboLog.date_time,
                                                             sm_role_code=nboLog.sm_role_code,
                                                             receipt_time=nboLog.receipt_time,
                                                             )
                                            try:
                                                url = globals.config_parser['connections']['post_logs_url']
                                                url = url[1:-1]
                                                putted = putToDb(url, type(nboDb).__name__, nboDb.user_login, json.dumps(
                                                    nboLogDB_toDict(nboDb), ensure_ascii=False))
                                                if putted == False:
                                                    print_sourceInfo(
                                                        "Failed to DB load", nboDb, nboLog.user_login, "-p")
                                            except Exception as e:
                                                print_errorInfo(e)
                                        else:
                                            globals.stats.raiseOthersCounter
                                    else:
                                        globals.stats.raiseOthersCounter
                                else:
                                    globals.stats.raiseOthersCounter
                            elif isNboResponseLog(log):
                                nboResponseLog = getNboResponseLog(log)
                                if nboResponseLog is not None:
                                    if isLoginExist(nboResponseLog):
                                        nboResponseLog = filterNboResponseLogByUser(
                                            nboResponseLog, users)
                                        nboResponseLog = filterNboResponseLogByChannel(
                                            nboResponseLog, globals.config_parser['filters']['channels'])
                                        nboResponseLog = filterNboResponseLogByGuid(
                                            nboResponseLog)
                                        nboResponseLog = filterNboResponseLogByOfferId(
                                            nboResponseLog)
                                        if nboResponseLog is not None:
                                            globals.stats.raiseNboResponseLogCounter
                                            nboResponseDb = NboResponseLogDB(trace_id=log.context_map.trace_id,
                                                                             gpb_guid=nboResponseLog.gpb_guid,
                                                                             user_login=nboResponseLog.user_login,
                                                                             offer_id=nboResponseLog.offer_id,
                                                                             offer_type=nboResponseLog.offer_type,
                                                                             product_code=nboResponseLog.product_code,
                                                                             product_name=nboResponseLog.product_name,
                                                                             response_name=nboResponseLog.response_name,
                                                                             reason_code=nboResponseLog.reason_code,
                                                                             reason_name=nboResponseLog.reason_name,
                                                                             receipt_time=nboResponseLog.receipt_time,
                                                                             response_time=nboResponseLog.response_time,
                                                                             created_at=log.created_at
                                                                             )
                                            try:
                                                url = globals.config_parser['connections']['post_logs_url']
                                                url = url[1:-1]
                                                putted = putToDb(url, type(nboResponseDb).__name__, nboResponseDb.user_login, json.dumps(
                                                    nboResponseLogDB_toDict(nboResponseDb), ensure_ascii=False))
                                                if putted == False:
                                                    print_sourceInfo(
                                                        "Failed to DB load", nboResponseDb, nboResponseLog.user_login, "-p")
                                            except Exception as e:
                                                print_errorInfo(e)
                                        else:
                                            globals.stats.raiseOthersCounter
                                    else:
                                        globals.stats.raiseOthersCounter
                                else:
                                    globals.stats.raiseOthersCounter
                            else:
                                globals.stats.raiseOthersCounter
                        else:
                            globals.stats.raiseOthersCounter
                        # print("KL #"+str(consumedCounter)+", where RA: "+str(clientLogCounter) + " | "+str(nboLogCounter) +
                        #       " | "+str(nboResponseLogCounter)+", EL: "+str(errorCounter)+", OL: "+str(othersCounter)+", Users: "+str(len(users)))
                    except Exception as e:
                        print_errorInfo("ExceptionMessage: " + e +
                                        ",\nObject: "+msg.value().decode('utf-8'))
                        globals.stats.raiseErrorCounter
                        pass
        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            self.consumer.close()
