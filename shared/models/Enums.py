from enum import Enum

class BillType(Enum):
    B = 1
    R = 2
    CR = 3
    JR = 4
    JRCA = 5
    EO = 6
    CA = 7
    M = 8
    CL = 9
    C = 10
    CSR = 11
    JM = 12
    P = 13
    SR = 14
    A = 15
    CM = 16
    I = 17
    PET = 18
    SB = 19
    IP = 20
    RB = 21
    RM = 22
    CB = 23

class EventType(Enum):
    HEARING = 1
    EXECUTIVE_SESSION = 2
    MARKUP_SESSION = 3

class MimeType(Enum):
    HTML = 1
    PDF = 2
    WORDPERFECT = 3
    MS_WORD = 4
    RTF = 5
    MS_WORD_2007 = 6

# class PoliticalParty(Enum):
#     DEMOCRAT = 1
#     REPUBLICAN = 2
#     INDEPENDENT = 3
#     GREEN_PARTY = 4
#     LIBERTARIAN = 5
#     NONPARTISAN = 6
    
class PoliticalParty(Enum):
    D = 1
    R = 2
    IND = 3
    G = 4
    L = 5
    NP = 6

class Reason(Enum):
    NEWBILL = 1
    STATUS_CHANGE = 2
    CHAMBER = 3
    COMPLETE = 4
    TITLE = 5
    DESCRIPTION = 6
    COMM_REFER = 7
    COMM_REPORT = 8
    SPONSOR_ADD = 9
    SPONSOR_REMOVE = 10
    SPONSOR_CHANGE = 11
    HISTORY_ADD = 12
    HISTORY_REMOVE = 13
    HISTORY_REVISED = 14
    HISTORY_MAJOR = 15
    HISTORY_MINOR = 16
    SUBJECT_ADD = 17
    SUBJECT_REMOVE = 18
    SAST = 19
    TEXT = 20
    AMENDMENT = 21
    SUPPLEMENT = 22
    VOTE = 23
    CALENDAR = 24
    PROGRESS = 25

class Role(Enum):
    REPRESENTATIVE = 1
    SENATOR = 2
    JOINT_CONFERENCE = 3

class SastType(Enum):
    SAME_AS = 1
    SIMILAR_TO = 2
    REPLACED_BY = 3
    REPLACES = 4
    CROSS_FILED = 5
    ENABLING_FOR = 6
    ENABLED_BY = 7
    RELATED = 8
    CARRY_OVER = 9

class SponsorType(Enum):
    GENERIC = 0
    PRIMARY = 1
    CO_SPONSOR = 2
    JOINT_SPONSOR = 3

class Stance(Enum):
    WATCH = 0
    SUPPORT = 1
    OPPOSE = 2

class Status(Enum):
    NA = 0
    INTRODUCED = 1
    ENGROSSED = 2
    ENROLLED = 3
    PASSED = 4
    VETOED = 5
    FAILED = 6
    OVERRIDE = 7
    CHAPTERED = 8
    REFER = 9
    REPORT_PASS = 10
    REPORT_DNP = 11
    DRAFT = 12

class SupplementType(Enum):
    FISCAL_NOTE = 1
    ANALYSIS = 2
    FISCAL_NOTE_ANALYSIS = 3
    VOTE_IMAGE = 4
    LOCAL_MANDATE = 5
    CORRECTIONS_IMPACT = 6
    MISCELLANEOUS = 7
    VETO_LETTER = 8

class TextType(Enum):
    INTRODUCED = 1
    COMMITTEE_SUBSTITUTE = 2
    AMENDED = 3
    ENGROSSED = 4
    ENROLLED = 5
    CHAPTERED = 6
    FISCAL_NOTE = 7
    ANALYSIS = 8
    DRAFT = 9
    CONFERENCE_SUBSTITUTE = 10
    PREFILED = 11
    VETO_MESSAGE = 12
    VETO_RESPONSE = 13
    SUBSTITUTE = 14

class VoteType(Enum):
    YEA = 1
    NAY = 2
    NOT_VOTING = 3
    ABSENT = 4