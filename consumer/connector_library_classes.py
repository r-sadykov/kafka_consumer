import json
from typing import Any
from consumer.connector_library_method_swamp import *


class Employee:
    full_name: str
    branch_name: str

    def __init__(self, full_name: str, branch_name: str) -> None:
        self.full_name = full_name
        self.branch_name = branch_name

    @staticmethod
    def from_dict(obj: Any) -> 'Employee':
        data = None
        if isinstance(obj, dict):
            data = obj
        else:
            data = json.loads(obj)
        full_name = from_stringified_bool(data.get("fullName"))
        branch_name = from_str(data.get("branchName"))
        return Employee(full_name, branch_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fullName"] = from_str(self.full_name)
        result["branchName"] = from_str(self.branch_name)
        return result


class ChannelMessageData:
    base_terminal_flag: bool
    data_list_size: int
    employee: Employee
    elapsed_time: int

    def __init__(self, base_terminal_flag: bool, data_list_size: int, employee: Employee, elapsed_time: int) -> None:
        self.base_terminal_flag = base_terminal_flag
        self.data_list_size = data_list_size
        self.employee = employee
        self.elapsed_time = elapsed_time

    @staticmethod
    def from_dict(obj: Any) -> 'ChannelMessageData':
        data = None
        if isinstance(obj, dict):
            data = obj
        else:
            data = json.loads(obj)
        base_terminal_flag = from_stringified_bool(
            from_str(data.get("baseTerminalFlag")))
        data_list_size = from_int(data.get("dataListSize"))
        employee = Employee.from_dict(data.get("employee"))
        elapsed_time = from_int(data.get("elapsedTime"))
        return ChannelMessageData(base_terminal_flag, data_list_size, employee, elapsed_time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["baseTerminalFlag"] = from_str(
            str(self.base_terminal_flag).lower())
        result["dataListSize"] = from_int(self.data_list_size)
        result["employee"] = to_class(Employee, self.employee)
        result["elapsedTime"] = from_int(self.elapsed_time)
        return result


class Categories:
    type: str
#    params: str   // возможно сняли

    def __init__(self, type: str) -> None:
        self.type = type
#        self.params = params

    @staticmethod
    def from_dict(obj: Any) -> 'Categories':
        data = None
        if isinstance(obj, dict):
            data = obj
        else:
            data = json.loads(obj)
        type = from_str(data.get("type"))
#        params = from_str(data.get("params"))
        return Categories(type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
#        result["params"] = from_str(self.params)
        return result


class Base:
    guid: str
    hid: int
    identity_type: int
    actual_date: str
    full_name: str
    surname: str
    name: str
    patronymic: str
    gender: str
    birth_place: str
    birth_settlement: str
    birth_rayon: str
    birth_region: str
    birth_country: str
    death_date: str
    bankruptcy: bool
    categories: List[Categories]
    residents: str
    citizenships: str
#    is_patronymic_lack: bool  // возможно сняли
    birthdate: str

    def __init__(self, guid: str, hid: int, identity_type: int, actual_date: str, full_name: str, surname: str, name: str, patronymic: str, gender: str, birth_place: str, birth_settlement: str, birth_rayon: str, birth_region: str, birth_country: str, death_date: str, bankruptcy: bool, categories: List[Categories], residents: str, citizenships: str, birthdate: str) -> None:
        self.guid = guid
        self.hid = hid
        self.identity_type = identity_type
        self.actual_date = actual_date
        self.full_name = full_name
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.gender = gender
        self.birth_place = birth_place
        self.birth_settlement = birth_settlement
        self.birth_rayon = birth_rayon
        self.birth_region = birth_region
        self.birth_country = birth_country
        self.death_date = death_date
        self.bankruptcy = bankruptcy
        self.categories = categories
        self.residents = residents
        self.citizenships = citizenships
#        self.is_patronymic_lack = is_patronymic_lack
        self.birthdate = birthdate

    @staticmethod
    def from_dict(obj: Any) -> 'Base':
        data = None
        if isinstance(obj, dict):
            data = obj
        else:
            data = json.loads(obj)
        guid = from_str(data.get("guid"))
        hid = int(from_str(data.get("hid")))
        identity_type = int(from_str(data.get("identityType")))
        actual_date = from_str(data.get("actualDate"))
        full_name = from_str(data.get("fullName"))
        surname = from_str(data.get("surname"))
        name = from_str(data.get("name"))
        patronymic = from_str(data.get("patronymic"))
        gender = from_str(data.get("gender"))
        birth_place = from_str(data.get("birthPlace"))
        birth_settlement = from_str(data.get("birthSettlement"))
        birth_rayon = from_str(data.get("birthRayon"))
        birth_region = from_str(data.get("birthRegion"))
        birth_country = from_str(data.get("birthCountry"))
        death_date = from_str(data.get("deathDate"))
        bankruptcy = from_stringified_bool(from_str(data.get("bankruptcy")))
        categories = from_list(Categories.from_dict, data.get("categories"))
        residents = from_str(data.get("residents"))
        citizenships = from_str(data.get("citizenships"))
 #       is_patronymic_lack = from_stringified_bool(
 #           from_str(data.get("isPatronymicLack")))
        birthdate = from_str(data.get("birthdate"))
        return Base(guid, hid, identity_type, actual_date, full_name, surname, name, patronymic, gender, birth_place, birth_settlement, birth_rayon, birth_region, birth_country, death_date, bankruptcy, categories, residents, citizenships, birthdate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["guid"] = from_str(self.guid)
        result["hid"] = from_str(str(self.hid))
        result["identityType"] = from_str(str(self.identity_type))
        result["actualDate"] = from_str(self.actual_date)
        result["fullName"] = from_str(self.full_name)
        result["surname"] = from_str(self.surname)
        result["name"] = from_str(self.name)
        result["patronymic"] = from_str(self.patronymic)
        result["gender"] = from_str(self.gender)
        result["birthPlace"] = from_str(self.birth_place)
        result["birthSettlement"] = from_str(self.birth_settlement)
        result["birthRayon"] = from_str(self.birth_rayon)
        result["birthRegion"] = from_str(self.birth_region)
        result["birthCountry"] = from_str(self.birth_country)
        result["deathDate"] = from_str(self.death_date)
        result["bankruptcy"] = from_str(str(self.bankruptcy).lower())
        result["categories"] = from_list(
            lambda x: to_class(Categories, x), self.categories)
        result["residents"] = from_str(self.residents)
        result["citizenships"] = from_str(self.citizenships)
#        result["isPatronymicLack"] = from_str(
#            str(self.is_patronymic_lack).lower())
        result["birthdate"] = from_str(self.birthdate)
        return result


class Client:
    base: Base
    addresses: str
    documents: str
    phones: str
    mails: str
    sources: str
    detail: str
    crs: str
    fatca: str
    entity_stoplist: str

    def __init__(self, base: Base, addresses: str, documents: str, phones: str, mails: str, sources: str, detail: str, crs: str, fatca: str, entity_stoplist: str) -> None:
        self.base = base
        self.addresses = addresses
        self.documents = documents
        self.phones = phones
        self.mails = mails
        self.sources = sources
        self.detail = detail
        self.crs = crs
        self.fatca = fatca
        self.entity_stoplist = entity_stoplist

    @staticmethod
    def from_dict(obj: Any) -> 'Client':
        data = None
        if isinstance(obj, dict):
            data = obj
        else:
            data = json.loads(obj)
        base = Base.from_dict(data.get("base"))
        addresses = from_str(data.get("addresses"))
        documents = from_str(data.get("documents"))
        phones = from_str(data.get("phones"))
        mails = from_str(data.get("mails"))
        sources = from_str(data.get("sources"))
        detail = from_str(data.get("detail"))
        crs = from_str(data.get("crs"))
        fatca = from_str(data.get("fatca"))
        entity_stoplist = from_str(data.get("entityStoplist"))
        return Client(base, addresses, documents, phones, mails, sources, detail, crs, fatca, entity_stoplist)

    def to_dict(self) -> dict:
        result: dict = {}
        result["base"] = to_class(Base, self.base)
        result["addresses"] = from_str(self.addresses)
        result["documents"] = from_str(self.documents)
        result["phones"] = from_str(self.phones)
        result["mails"] = from_str(self.mails)
        result["sources"] = from_str(self.sources)
        result["detail"] = from_str(self.detail)
        result["crs"] = from_str(self.crs)
        result["fatca"] = from_str(self.fatca)
        result["entityStoplist"] = from_str(self.entity_stoplist)
        return result


class BodyData:
    clients: List[Client]

    def __init__(self, clients: List[Client]) -> None:
        self.clients = clients

    @staticmethod
    def from_dict(obj: Any) -> 'BodyData':
        data = None
        if isinstance(obj, dict):
            data = obj
        else:
            data = json.loads(obj)
        clients = from_list(Client.from_dict, data.get("clients"))
        return BodyData(clients)

    def to_dict(self) -> dict:
        result: dict = {}
        result["clients"] = from_list(
            lambda x: to_class(Client, x), self.clients)
        return result


class Body:
    status: str
    actual_timestamp: str
    data: BodyData

    def __init__(self, status: str, actual_timestamp: str, data: BodyData) -> None:
        self.status = status
        self.actual_timestamp = actual_timestamp
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> 'Body':
        data = None
        if isinstance(obj, dict):
            data = obj
        else:
            data = json.loads(obj)
        status = from_str(data.get("status"))
        actual_timestamp = from_str(data.get("actualTimestamp"))
        data = BodyData.from_dict(data.get("data"))
        return Body(status, actual_timestamp, data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = from_str(self.status)
        result["actualTimestamp"] = from_str(self.actual_timestamp)
        result["data"] = to_class(BodyData, self.data)
        return result


class ClientLog:
    channel: str
    bff_path: str
    guid: str
    data: ChannelMessageData
    request_id: str
    office_code: str
    branch_code: str
    full_url: str
    body: Body
    http_headers: str
    http_status_code: int
    actual_timestamp: int
    login: str

    def __init__(self, channel: str, bff_path: str, guid: str, data: ChannelMessageData, request_id: str, office_code: str, branch_code: str, full_url: str, body: Body, http_headers: str, http_status_code: int, actual_timestamp: int, login: str) -> None:
        self.channel = channel
        self.bff_path = bff_path
        self.guid = guid
        self.data = data
        self.request_id = request_id
        self.office_code = office_code
        self.branch_code = branch_code
        self.full_url = full_url
        self.body = body
        self.http_headers = http_headers
        self.http_status_code = http_status_code
        self.actual_timestamp = actual_timestamp
        self.login = login

    @staticmethod
    def from_dict(obj: Any) -> 'ClientLog':
        assert isinstance(obj, dict)
        channel = from_str(obj.get("channel"))
        bff_path = from_str(obj.get("bffPath"))
        guid = from_str(obj.get("guid"))
        data = ChannelMessageData.from_dict(obj.get("data"))
        request_id = from_str(obj.get("requestId"))
        office_code = from_str(obj.get("officeCode"))
        branch_code = from_str(obj.get("branchCode"))
        full_url = from_str(obj.get("fullUrl"))
        body = Body.from_dict(obj.get("body"))
        http_headers = from_str(obj.get("httpHeaders"))
        http_status_code = int(from_str(obj.get("httpStatusCode")))
        actual_timestamp = from_int(obj.get("actualTimestamp"))
        login = from_str(obj.get("login"))
        return ClientLog(channel, bff_path, guid, data, request_id, office_code, branch_code, full_url, body, http_headers, http_status_code, actual_timestamp, login)

    def to_dict(self) -> dict:
        result: dict = {}
        result["channel"] = from_str(self.channel)
        result["bffPath"] = from_str(self.bff_path)
        result["guid"] = from_str(self.guid)
        result["data"] = to_class(ChannelMessageData, self.data)
        result["requestId"] = from_str(self.request_id)
        result["officeCode"] = from_str(self.office_code)
        result["branchCode"] = from_str(self.branch_code)
        result["fullUrl"] = from_str(self.full_url)
        result["body"] = to_class(Body, self.body)
        result["httpHeaders"] = from_str(self.http_headers)
        result["httpStatusCode"] = from_str(str(self.http_status_code))
        result["actualTimestamp"] = from_int(self.actual_timestamp)
        result["login"] = from_str(self.login)
        return result


class CategoriesDB:
    type: str

    def __init__(self, type: str) -> None:
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'CategoriesDB':
        data = None
        if isinstance(obj, dict):
            data = obj
        else:
            data = json.loads(obj)
        type = from_str(data.get("type"))
        return Categories(type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        return result


class ClientLogDB:
    client_guid: str
    response_status: str
    body_actual_timestamp: str
    trace_id: str
    login: str
    categories: List[CategoriesDB]

    def __init__(self, client_guid: str, response_status: str, body_actual_timestamp: str,
                 trace_id: str, login: str, categories: List[CategoriesDB], created_at: str, clients_quantity: str) -> None:
        self.client_guid = client_guid
        self.response_status = response_status
        self.body_actual_timestamp = body_actual_timestamp
        self.trace_id = trace_id
        self.created_at = created_at
        self.login = login
        self.categories = categories
        self.clients_quantity = clients_quantity

    @staticmethod
    def from_dict(obj: Any) -> 'ClientLogDB':
        assert isinstance(obj, dict)
        client_guid = from_str(obj.get("clientGuid"))
        response_status = from_str(obj.get("responseStatus"))
        body_actual_timestamp = from_str(obj.get("bodyActualTimestamp"))
        trace_id = from_str(obj.get("traceId"))
        login = from_str(obj.get("login"))
        created_at = from_str(obj.get('createdAt'))
        categories = from_list(CategoriesDB.from_dict, obj.get("categories"))
        clients_quantity = from_int(obj.get("clientsQuantity"))
        return ClientLogDB(client_guid, response_status, body_actual_timestamp, trace_id, login, categories, created_at, clients_quantity)

    def to_dict(self) -> dict:
        result: dict = {}
        result["clientGuid"] = from_str(self.client_guid)
        result["responseStatus"] = from_str(self.response_status)
        result["bodyActualTimestamp"] = from_str(self.body_actual_timestamp)
        result["traceId"] = from_str(self.trace_id)
        result["login"] = from_str(self.login)
        result["categories"] = from_list(
            lambda x: to_class(CategoriesDB, x), self.categories)
        result["createdAt"] = from_str(self.created_at)
        result["clientsQuantity"] = from_int(self.clients_quantity)
        return result


class NboWithResponseLog:
    gpb_guid: str
    gpb_request_id: str
    date_time: datetime
    response_time: datetime
    contact_id: str
    offer_id: str
    offer_name: str
    offer_type: str
    product_code: str
    product_name: str
    product_type: str
    user_name: str
    user_login: str
    priority: int
    type: str
    response_code: str
    response_name: str
    reason_code: str
    reason_name: str
    receipt_time: str
    elapsed_time: int
    user_office: str
    channel: str
    sm_role_code: str
    banner_id: str
    error_code: str

    def __init__(self, gpb_guid: str, gpb_request_id: str, date_time: str,
                 response_time: str, contact_id: str, offer_id: str, offer_name: str, offer_type: str,
                 product_code: str, product_name: str, product_type: str, user_name: str, user_login: str,
                 priority: int, type: str, response_code: str, response_name: str, reason_code: str, reason_name: str,
                 receipt_time: str, elapsed_time: int, user_office: str, channel: str, sm_role_code: str,
                 banner_id: str, error_code: str) -> None:
        self.gpb_guid = gpb_guid
        self.gpb_request_id = gpb_request_id
        self.date_time = date_time
        self.response_time = response_time
        self.contact_id = contact_id
        self.offer_id = offer_id
        self.offer_name = offer_name
        self.offer_type = offer_type
        self.product_code = product_code
        self.product_name = product_name
        self.product_type = product_type
        self.user_name = user_name
        self.user_login = user_login
        self.priority = priority
        self.type = type
        self.response_code = response_code
        self.response_name = response_name
        self.reason_code = reason_code
        self.reason_name = reason_name
        self.receipt_time = receipt_time
        self.elapsed_time = elapsed_time
        self.user_office = user_office
        self.channel = channel
        self.sm_role_code = sm_role_code
        self.banner_id = banner_id
        self.error_code = error_code

    @staticmethod
    def from_dict(obj: Any) -> 'NboWithResponseLog':
        assert isinstance(obj, dict)
        gpb_guid = from_str(obj.get("gpbGuid"))
        gpb_request_id = from_str(obj.get("gpbRequestId"))
        if obj.get("dateTime") is not None:
            date_time = from_datetime(obj.get("dateTime"))
        else:
            date_time = None
        if obj.get("responseTime") is not None:
            response_time = from_datetime(obj.get("responseTime"))
        else:
            response_time = None
        if obj.get("contactId") is not None:
            contact_id = from_str(obj.get("contactId"))
        else:
            contact_id = None
        if obj.get("offerId") is not None:
            offer_id = from_str(obj.get("offerId"))
        else:
            offer_id = None
        if obj.get("offerName") is not None:
            offer_name = from_str(obj.get("offerName"))
        else:
            offer_name = None
        if obj.get("offerType") is not None:
            offer_type = from_str(obj.get("offerType"))
        else:
            offer_type = None
        if obj.get("productCode") is not None:
            product_code = from_str(obj.get("productCode"))
        else:
            product_code = None
        if obj.get("productName") is not None:
            product_name = from_str(obj.get("productName"))
        else:
            product_name = None
        if obj.get("productType") is not None:
            product_type = from_str(obj.get("productType"))
        else:
            product_type = None
        if obj.get("userName") is not None:
            user_name = from_str(obj.get("userName"))
        else:
            user_name = None
        user_login = from_str(obj.get("userLogin"))
        if obj.get("priority") is not None:
            priority = int(from_str(obj.get("priority")))
        else:
            priority = None
        if obj.get("type") is not None:
            type = from_str(obj.get("type"))
        else:
            type = None
        if obj.get("responseCode") is not None:
            response_code = from_str(obj.get("responseCode"))
        else:
            response_code = None
        if obj.get("responseName") is not None:
            response_name = from_str(obj.get("responseName"))
        else:
            response_name = None
        if obj.get("reasonCode") is not None:
            reason_code = from_str(obj.get("reasonCode"))
        else:
            reason_code = None
        if obj.get("reasonName") is not None:
            reason_name = from_str(obj.get("reasonName"))
        else:
            reason_name = None
        if obj.get("receiptTime") is not None:
            receipt_time = from_str(obj.get("receiptTime"))
        else:
            receipt_time = None
        elapsed_time = from_int(obj.get("elapsedTime"))
        if obj.get("userOffice") is not None:
            user_office = from_str(obj.get("userOffice"))
        else:
            user_office = None
        channel = from_str(obj.get("channel"))
        if obj.get("smRoleCode") is not None:
            sm_role_code = from_str(obj.get("smRoleCode"))
        else:
            sm_role_code = None
        if obj.get("bannerId") is not None:
            banner_id = from_str(obj.get("bannerId"))
        else:
            banner_id = None
        if obj.get("errorCode") is not None:
            error_code = from_str(obj.get("errorCode"))
        else:
            error_code = None
        return NboWithResponseLog(gpb_guid, gpb_request_id, date_time,
                                  response_time, contact_id, offer_id, offer_name, offer_type,
                                  product_code, product_name, product_type,
                                  user_name, user_login, priority,
                                  type, response_code, response_name, reason_code, reason_name, receipt_time,
                                  elapsed_time, user_office, channel, sm_role_code, banner_id, error_code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["gpbGuid"] = from_str(self.gpb_guid)
        result["gpbRequestId"] = from_str(self.gpb_request_id)
        if self.date_time is not None:
            result["dateTime"] = self.date_time.isoformat()
        else:
            result["dateTime"] = None
        if self.response_time is not None:
            result["responseTime"] = self.response_time.isoformat()
        else:
            result["responseTime"] = None
        result["contactId"] = from_str(self.contact_id)
        result["offerId"] = from_str(self.offer_id)
        result["offerName"] = from_str(self.offer_name)
        result["offerType"] = from_str(self.offer_type)
        result["productCode"] = from_str(self.product_code)
        result["productName"] = from_str(self.product_name)
        result["productType"] = from_str(self.product_type)
        result["userName"] = from_str(self.user_name)
        result["userLogin"] = from_str(self.user_login)
        result["priority"] = from_str(str(self.priority))
        result["type"] = from_str(self.type)
        result["responseCode"] = from_str(self.response_code)
        result["responseName"] = from_str(self.response_name)
        result["reasonCode"] = from_str(self.reason_code)
        result["reasonName"] = from_str(self.reason_name)
        result["receiptTime"] = from_str(self.receipt_time)
        result["elapsedTime"] = from_int(self.elapsed_time)
        result["userOffice"] = from_str(self.user_office)
        result["channel"] = from_str(self.channel)
        result["smRoleCode"] = from_str(self.sm_role_code)
        result["bannerId"] = from_str(self.banner_id)
        result["errorCode"] = from_str(self.error_code)
        return result


class Instant:
    epoch_second: int
    nano_of_second: int

    def __init__(self, epoch_second: int, nano_of_second: int) -> None:
        self.epoch_second = epoch_second
        self.nano_of_second = nano_of_second

    @staticmethod
    def from_dict(obj: Any) -> 'Instant':
        assert isinstance(obj, dict)
        epoch_second = from_int(obj.get("epochSecond"))
        nano_of_second = from_int(obj.get("nanoOfSecond"))
        return Instant(epoch_second, nano_of_second)

    def to_dict(self) -> dict:
        result: dict = {}
        result["epochSecond"] = from_int(self.epoch_second)
        result["nanoOfSecond"] = from_int(self.nano_of_second)
        return result


class ContextMap:
    span_id: str
    trace_id: str

    def __init__(self, span_id: str, trace_id: str) -> None:
        self.span_id = span_id
        self.trace_id = trace_id

    @staticmethod
    def from_dict(obj: Any) -> 'ContextMap':
        assert isinstance(obj, dict)
        if 'span_id' in obj:
            span_id = from_str(obj['span_id'])
        else:
            span_id = ""
        trace_id = from_str(obj.get("traceId"))
        return ContextMap(span_id, trace_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["spanId"] = from_str(self.span_id)
        result["traceId"] = from_str(self.trace_id)
        return result


class KafkaLog:
    instant: Instant
    thread: str
    level: str
    logger_name: str
    message: str
    end_of_batch: bool
    logger_fqcn: str
    context_map: ContextMap
    thread_id: int
    thread_priority: int
    created_at: str
    host_name: str
    app_name: str
    src_name: str
    service_id: str

    def __init__(self, instant: Instant, thread: str, level: str, logger_name: str, message: str, end_of_batch: bool, logger_fqcn: str, context_map: ContextMap, thread_id: int, thread_priority: int, created_at: str, host_name: str, app_name: str, src_name: str, service_id: str) -> None:
        self.instant = instant
        self.thread = thread
        self.level = level
        self.logger_name = logger_name
        self.message = message
        self.end_of_batch = end_of_batch
        self.logger_fqcn = logger_fqcn
        self.context_map = context_map
        self.thread_id = thread_id
        self.thread_priority = thread_priority
        self.created_at = created_at
        self.host_name = host_name
        self.app_name = app_name
        self.src_name = src_name
        self.service_id = service_id

    @staticmethod
    def from_dict(obj: Any) -> 'KafkaLog':
        assert isinstance(obj, dict)
        instant = Instant.from_dict(obj.get("instant"))
        thread = from_str(obj.get("thread"))
        level = from_str(obj.get("level"))
        logger_name = from_str(obj.get("loggerName"))
        message = from_str(obj.get("message"))
        end_of_batch = from_bool(obj.get("endOfBatch"))
        logger_fqcn = from_str(obj.get("loggerFqcn"))
        context_map = ContextMap.from_dict(obj.get("contextMap"))
        thread_id = from_int(obj.get("threadId"))
        thread_priority = from_int(obj.get("threadPriority"))
        created_at = from_str(obj.get("createdAt"))
        host_name = from_str(obj.get("hostName"))
        app_name = from_str(obj.get("appName"))
        src_name = from_str(obj.get("srcName"))
        service_id = from_str(obj.get("service-id"))
        return KafkaLog(instant, thread, level, logger_name, message, end_of_batch, logger_fqcn, context_map, thread_id, thread_priority, created_at, host_name, app_name, src_name, service_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["instant"] = to_class(Instant, self.instant)
        result["thread"] = from_str(self.thread)
        result["level"] = from_str(self.level)
        result["loggerName"] = from_str(self.logger_name)
        result["message"] = from_str(self.message)
        result["endOfBatch"] = from_bool(self.end_of_batch)
        result["loggerFqcn"] = from_str(self.logger_fqcn)
        result["contextMap"] = to_class(ContextMap, self.context_map)
        result["threadId"] = from_int(self.thread_id)
        result["threadPriority"] = from_int(self.thread_priority)
        result["createdAt"] = from_str(self.created_at)
        result["hostName"] = from_str(self.host_name)
        result["appName"] = from_str(self.app_name)
        result["srcName"] = from_str(self.src_name)
        result["service-id"] = from_str(self.service_id)
        return result


class NboLogDB:
    trace_id: str
    gpb_guid: str
    user_login: str
    created_at: str
    contact_id: str
    offer_id: str
    product_code: str
    product_name: str
    priority: int
    date_time: datetime
    sm_role_code: str
    receipt_time: str

    def __init__(self, trace_id: str, gpb_guid: str, user_login: str, created_at: str, contact_id: str, offer_id: str,
                 product_code: str,product_name: str, priority: int, date_time: str, sm_role_code: str, receipt_time: str) -> None:
        self.trace_id = trace_id
        self.gpb_guid = gpb_guid
        self.user_login = user_login
        self.created_at = created_at
        self.contact_id = contact_id
        self.offer_id = offer_id
        self.product_code=product_code
        self.product_name = product_name
        self.priority = priority
        self.date_time = date_time
        self.sm_role_code = sm_role_code
        self.receipt_time = receipt_time

    @staticmethod
    def from_dict(obj: Any) -> 'NboLogDB':
        assert isinstance(obj, dict)
        trace_id = from_str(obj.get("traceId"))
        gpb_guid = from_str(obj.get("gpbGuid"))
        user_login = from_str(obj.get("userLogin"))
        created_at = from_str(obj.get("createdAt"))
        contact_id = from_str(obj.get("contactId"))
        offer_id = from_str(obj.get("offerId"))
        product_code=from_str(obj.get("productCode"))
        product_name = from_str(obj.get("productName"))
        priority = from_str(obj.get("priority"))
        date_time = from_datetime(obj.get("dateTime"))
        sm_role_code = from_str(obj.get("smRoleCode"))
        receipt_time = from_str(obj.get("receiptTime"))

        return NboLogDB(trace_id, gpb_guid, user_login, created_at, contact_id, offer_id, product_code,product_name, priority,
                        date_time, sm_role_code, receipt_time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["traceId"] = from_str(self.trace_id)
        result["gpbGuid"] = from_str(self.gpb_guid)
        result["userLogin"] = from_str(self.user_login)
        result["createdAt"] = from_str(self.created_at)
        result["contactId"] = from_str(self.contact_id)
        result["offerId"] = from_str(self.offer_id)
        result["productCode"] = from_str(self.product_code)
        result["productName"] = from_str(self.product_name)
        result["priority"] = from_str(str(self.priority))
        result["dateTime"] = self.date_time.isoformat()
        result["smRoleCode"] = from_str(self.sm_role_code)
        result["receiptTime"] = from_str(self.receipt_time)
        return result


class NboResponseLogDB:
    trace_id: str
    gpb_guid: str
    user_login: str
    offer_id: str
    offer_type: str
    product_code: str
    product_name: str
    response_name: str
    reason_code: str
    reason_name: str
    receipt_time: str
    response_time: datetime
    created_at: str

    def __init__(self, trace_id: str, gpb_guid: str, user_login: str, offer_id: str, offer_type: str,
                 product_code:str,product_name: str, response_name: str, reason_code: str, reason_name: str,
                 receipt_time: str, response_time: str, created_at: str) -> None:
        self.trace_id = trace_id
        self.gpb_guid = gpb_guid
        self.user_login = user_login
        self.offer_id = offer_id
        self.offer_type = offer_type
        self.product_code = product_code
        self.product_name = product_name
        self.response_name = response_name
        self.reason_code = reason_code
        self.reason_name = reason_name
        self.receipt_time = receipt_time
        self.response_time = response_time
        self.created_at = created_at

    @staticmethod
    def from_dict(obj: Any) -> 'NboResponseLogDB':
        assert isinstance(obj, dict)
        trace_id = from_str(obj.get("traceId"))
        gpb_guid = from_str(obj.get("gpbGuid"))
        user_login = from_str(obj.get("userLogin"))
        offer_id = from_str(obj.get("offerId"))
        offer_type = from_str(obj.get("offerType"))
        product_code = from_str(obj.get("productCode"))
        product_name = from_str(obj.get("productName"))
        response_name = from_str(obj.get("responseName"))
        reason_code = from_str(obj.get("reasonCode"))
        reason_name = from_str(obj.get("reasonName"))
        receipt_time = from_str(obj.get("receiptTime"))
        response_time = from_datetime(obj.get("responseTime"))
        created_at = from_str(obj.get("createdAt"))

        return NboResponseLogDB(trace_id, gpb_guid, user_login, offer_id, offer_type, product_code,product_name,
                                response_name, reason_code, reason_name, receipt_time, response_time, created_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result['traceId'] = from_str(self.trace_id)
        result["gpbGuid"] = from_str(self.gpb_guid)
        result["userLogin"] = from_str(self.user_login)
        result["offerId"] = from_str(self.offer_id)
        result["offerType"] = from_str(self.offer_type)
        result["productCode"] = from_str(self.product_code)
        result["productName"] = from_str(self.product_name)
        result["responseName"] = from_str(self.response_name)
        result["reasonCode"] = from_str(self.reason_code)
        result["reasonName"] = from_str(self.reason_name)
        result["receiptTime"] = from_str(self.receipt_time)
        result["responseTime"] = self.response_time.isoformat()
        result["createdAt"] = from_str(self.created_at)
        return result


def clientLog_fromDict(s: Any) -> ClientLog:
    return ClientLog.from_dict(s)


def clientLog_toDict(x: ClientLog) -> Any:
    return to_class(ClientLog, x)


def clientLogDB_fromDict(s: Any) -> ClientLogDB:
    return ClientLogDB.from_dict(s)


def clientLogDB_toDict(x: ClientLogDB) -> Any:
    return to_class(ClientLogDB, x)


def encapsulate(categories: Categories) -> CategoriesDB:
    categories_db = []
    for item in categories:
        categories_db.append(CategoriesDB(item.type))
    return categories_db


def nboWithResponseLog_fromDict(s: Any) -> NboWithResponseLog:
    return NboWithResponseLog.from_dict(s)


def nboWithResponseLog_toDict(x: NboWithResponseLog) -> Any:
    return to_class(NboWithResponseLog, x)


def kafkaLog_fromDict(s: Any) -> KafkaLog:
    return KafkaLog.from_dict(s)


def kafkaLog_toDict(x: KafkaLog) -> Any:
    return to_class(KafkaLog, x)


def nboLogDB_fromDict(s: Any) -> NboLogDB:
    return NboLogDB.from_dict(s)


def nboLogDB_toDict(x: NboLogDB) -> Any:
    return to_class(NboLogDB, x)


def nboResponseLogDB_fromDict(s: Any) -> NboResponseLogDB:
    return NboResponseLogDB.from_dict(s)


def nboResponseLogDB_toDict(x: NboResponseLogDB) -> Any:
    return to_class(NboResponseLogDB, x)
