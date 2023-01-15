import os
from confluent_kafka import Consumer, OFFSET_BEGINNING
import consumer.connector_globals as globals
from consumer.connector_http import putToDb
from consumer.connector_logger import *
from consumer.connector_methods import *


class KafkaConsumerTester:
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
        noneLogCounter = 0
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
                        if log is not None:
                            print_text(
                                "Kafka", "Read object from Kafka server", get_stringFromItem(log))
                            consumedCounter += 1
                            if isClientLog(log):
                                print_text(
                                    "ClientLog", "after isClientLog method", "OK")
                                clientLog = getClientLog(log)
                                print_text(
                                    "ClientLog", "after getClientLog", get_stringFromItem(clientLog))
                                if clientLog is not None:
                                    if isLoginExist(clientLog):
                                        print_text(
                                            "ClientLog", "after isLogin filter", get_stringFromItem(clientLog))
                                        clientLog = filterClientLogByUser(
                                            clientLog, users)
                                        print_text(
                                            "ClientLog", "after User filter", get_stringFromItem(clientLog))
                                        clientLog = filterClientLogByChannel(
                                            clientLog, globals.config_parser['filters']['channels'])
                                        print_text(
                                            "ClientLog", "after Channel filter", get_stringFromItem(clientLog))
                                        clientLog = filterClientLogByUrl(
                                            clientLog, globals.config_parser['filters']['client_log_url'])
                                        print_text(
                                            "ClientLog", "after URL filter", get_stringFromItem(clientLog))
                                        clientLog = filterClientLogBySize(
                                            clientLog, 1)
                                        print_text(
                                            "ClientLog", "after Size filter", get_stringFromItem(clientLog))
                                        clientLog = filterClientLogByStatus(
                                            clientLog, 'success')
                                        print_text(
                                            "ClientLog", "after Status filter", get_stringFromItem(clientLog))
                                        clientLog = filterClientLogByGuid(
                                            clientLog)
                                        print_text(
                                            "ClientLog", "after GUID filter", get_stringFromItem(clientLog))
                                        if clientLog is not None:
                                            clientLogCounter += 1
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
                                            print_text(
                                                "ClientLog", "ClientLog formed to transfer into DB", get_stringFromItem(clientDb))
                                        else:
                                            othersCounter += 1
                                    else:
                                        othersCounter += 1
                                else:
                                    othersCounter += 1
                            elif isNboLog(log):
                                print_text(
                                    "NboLog", "after isNboLog method", "OK")
                                nboLog = getNboLog(log)
                                print_text(
                                    "NboLog", "after getNboLog method", get_stringFromItem(nboLog))
                                if nboLog is not None:
                                    if isLoginExist(nboLog):
                                        print_text(
                                            "NboLog", "after isLogin filter", get_stringFromItem(nboLog))
                                        nboLog = filterNboLogByUser(
                                            nboLog, users)
                                        print_text(
                                            "NboLog", "after User filter", get_stringFromItem(nboLog))
                                        nboLog = filterNboLogByChannel(
                                            nboLog, globals.config_parser['filters']['channels'])
                                        print_text(
                                            "NboLog", "after Channel filter", get_stringFromItem(nboLog))
                                        nboLog = filterNboLogByGuid(nboLog)
                                        print_text(
                                            "NboLog", "after GUID filter", get_stringFromItem(nboLog))
                                        nboLog = filterNboLogByOfferId(nboLog)
                                        print_text(
                                            "NboLog", "after OfferID filter", get_stringFromItem(nboLog))
                                        if nboLog is not None:
                                            nboLogCounter += 1
                                            nboDb = NboLogDB(trace_id=log.context_map.trace_id,
                                                             gpb_guid=nboLog.gpb_guid,
                                                             user_login=nboLog.user_login,
                                                             created_at=log.created_at,
                                                             contact_id=nboLog.contact_id,
                                                             offer_id=nboLog.offer_id,
                                                             product_name=nboLog.product_name,
                                                             priority=nboLog.priority,
                                                             date_time=nboLog.date_time,
                                                             sm_role_code=nboLog.sm_role_code,
                                                             receipt_time=nboLog.receipt_time,
                                                             )
                                            print_text(
                                                "NboLog", "NboLog formed to transfer into DB", get_stringFromItem(nboDb))
                                        else:
                                            othersCounter += 1
                                    else:
                                        othersCounter += 1
                                else:
                                    othersCounter += 1
                            elif isNboResponseLog(log):
                                print_text(
                                    "NboResponseLog", "after isNboResponseLog method", "OK")
                                nboResponseLog = getNboResponseLog(log)
                                print_text(
                                    "NboResponseLog", "after getNboResponseLog method", get_stringFromItem(nboResponseLog))
                                if nboResponseLog is not None:
                                    if isLoginExist(nboResponseLog):
                                        print_text(
                                            "NboResponseLog", "after isLogin filter", get_stringFromItem(nboResponseLog))
                                        nboResponseLog = filterNboResponseLogByUser(
                                            nboResponseLog, users)
                                        print_text(
                                            "NboResponseLog", "after User filter", get_stringFromItem(nboResponseLog))
                                        nboResponseLog = filterNboResponseLogByChannel(
                                            nboResponseLog, globals.config_parser['filters']['channels'])
                                        print_text(
                                            "NboResponseLog", "after Channel filter", get_stringFromItem(nboResponseLog))
                                        nboResponseLog = filterNboResponseLogByGuid(
                                            nboResponseLog)
                                        print_text(
                                            "NboResponseLog", "after GUID filter", get_stringFromItem(nboResponseLog))
                                        nboResponseLog = filterNboResponseLogByOfferId(
                                            nboResponseLog)
                                        print_text(
                                            "NboResponseLog", "after OfferID filter", get_stringFromItem(nboResponseLog))
                                        if nboResponseLog is not None:
                                            nboResponseLogCounter += 1
                                            nboResponseDb = NboResponseLogDB(trace_id=log.context_map.trace_id,
                                                                             gpb_guid=nboResponseLog.gpb_guid,
                                                                             user_login=nboResponseLog.user_login,
                                                                             offer_id=nboResponseLog.offer_id,
                                                                             offer_type=nboResponseLog.offer_type,
                                                                             product_name=nboResponseLog.product_name,
                                                                             response_name=nboResponseLog.response_name,
                                                                             reason_code=nboResponseLog.reason_code,
                                                                             reason_name=nboResponseLog.reason_name,
                                                                             receipt_time=nboResponseLog.receipt_time,
                                                                             response_time=nboResponseLog.response_time,
                                                                             created_at=log.created_at
                                                                             )
                                            print_text(
                                                "NboResponseLog", "NboResponseLog formed to transfer into DB", get_stringFromItem(nboResponseDb))
                                        else:
                                            othersCounter += 1
                                    else:
                                        othersCounter += 1
                                else:
                                    othersCounter += 1
                            else:
                                othersCounter += 1
                        else:
                            noneLogCounter += 1
                        print("KL #"+str(consumedCounter)+", where RA: "+str(clientLogCounter) + " | "+str(nboLogCounter) +
                              " | "+str(nboResponseLogCounter)+", N/A: " + str(noneLogCounter)+", EL: "+str(errorCounter)+", OL: "+str(othersCounter)+", Users: "+str(len(users)))
                        if clientLogCounter == 100:
                            break
                    except Exception as e:
                        print_errorInfo("ExceptionMessage: " + e +
                                        ",\nObject: "+msg.value().decode('utf-8'))
                        errorCounter += 1
                        pass
        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            self.consumer.close()
