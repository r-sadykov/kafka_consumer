from typing import List
from consumer.connector_library_classes import *


def filterClientLogByUser(clientLog: ClientLog, users: List[str]):
    if clientLog is None:
        return None
    if clientLog.login in users:
        return clientLog
    return None


def filterNboLogByUser(nboLog: NboWithResponseLog, users: List[str]):
    if nboLog is None:
        return None
    if nboLog.user_login in users:
        return nboLog
    return None


def filterNboResponseLogByUser(nboResponseLog: NboWithResponseLog, users: List[str]):
    return filterNboLogByUser(nboResponseLog, users)


def filterClientLogByChannel(clientLog: ClientLog, channels: List[str]):
    if clientLog is None:
        return None
    if clientLog.channel in channels:
        return clientLog
    return None


def filterNboLogByChannel(nboLog: NboWithResponseLog, channels: List[str]):
    if nboLog is None:
        return None
    if nboLog.channel in channels:
        return nboLog
    return None


def filterNboResponseLogByChannel(nboResponseLog: NboWithResponseLog, channels: List[str]):
    if nboResponseLog is None:
        return None
    if nboResponseLog.channel in channels:
        return nboResponseLog
    return None


def filterClientLogByUrl(clientLog: ClientLog, url: str):
    if clientLog is None:
        return None
    if url in clientLog.full_url:
        return clientLog
    return None


def filterClientLogBySize(clientLog: ClientLog, size: int):
    if clientLog is None:
        return None
    if clientLog.data.data_list_size == size:
        return clientLog
    return None


def filterClientLogByStatus(clientLog: ClientLog, status: str):
    if clientLog is None:
        return None
    if clientLog.body.status == status:
        return clientLog
    return None


def filterClientLogByGuid(clientLog: ClientLog):
    if clientLog is None:
        return None
    if clientLog.guid != "" and clientLog.guid != None:
        return clientLog
    return None


def filterNboLogByGuid(nboLog: NboWithResponseLog):
    if nboLog is None:
        return None
    if nboLog.gpb_guid != "" and nboLog.gpb_guid != None:
        return nboLog
    return None


def filterNboResponseLogByGuid(nboResponseLog):
    return filterNboLogByGuid(nboResponseLog)


def filterNboLogByOfferId(nboLog: NboWithResponseLog):
    if nboLog is None:
        return None
    if nboLog.offer_id != "" and nboLog.offer_id != None:
        return nboLog
    return None


def filterNboResponseLogByOfferId(nboResponseLog):
    return filterNboLogByOfferId(nboResponseLog)
