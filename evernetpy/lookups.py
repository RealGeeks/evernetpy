from collections import defaultdict
from evernetpy.execute import execute_listing_query
from evernetpy.memoize import memoize

office_name_cache = {}

FIXED_NWMLS_LOOKUPS = {
    'ST': {
        'A': 'Active',
        'CT': 'Contingent',
        'PB': 'Pending BU Requested',
        'PF': 'Pending Feasability',
        'PI': 'Pending Inspection',
        'PS': 'Pending Short Sale',
        'P': 'Pending',
        'E': 'Expired',
        'T': 'Temp. Off Markt.',
        'SFR': 'Sale Fail Release',
        'CA': 'Cancelled',
        'R': 'Rented',
        'S': 'Sold',
    },
    'SD': {
        '00':'Not Known',
        'ABR':'Aberdeen',
        'AD':'Adna',
        'ALMI':'Almira',
        'ANA':'Anacortes',
        'AR':'Arlington',
        'ASOT':'Asotin-Anatone',
        'AUB':'Auburn',
        'BE':'Bellevue',
        'BEL':'Bellingham',
        'BENG':'Benge',
        'BG':'Battle Ground',
        'BICK':'Bickleton',
        'BIS':'Bainbridge Island',
        'BLN':'Blaine',
        'BOI':'Boistfort',
        'BRG':'Bridgeport',
        'BRI':'Brinnon',
        'BRL':'Burlington',
        'BRM':'Bremerton #100c',
        'BRW':'Brewster',
        'BTH':'Bethel',
        'CAM':'Camas',
        'CAS':'Cashmere',
        'CEN':'Centralia',
        'CENT':'Centerville',
        'CENV':'Central Valley',
        'CHE':'Chehalis',
        'CHEN':'Cheney',
        'CHEW':'Chewelah',
        'CHI':'Chimacum #49',
        'CK':'Central Kitsap #401',
        'CLAR':'Clarkston',
        'CLE':'Cle Elum-Roslyn',
        'CLH':'Coulee-Hartline',
        'CLP':'Clover Park',
        'COFX':'Colfax',
        'COLB':'Columbia - Burbank',
        'COLH':'Columbia - Hunters',
        'COLP':'College Place',
        'COLT':'Colton',
        'COLV':'Colville',
        'CON':'Concrete',
        'COS':'Cosmopolis',
        'CPF':'Cape Flattery',
        'CPV':'Coupeville',
        'CRB':'Carbonado',
        'CRE':'Creston',
        'CRES':'Crescent',
        'CRK':'Castle Rock',
        'CSC':'Cascade',
        'CURL':'Curlew',
        'CUSI':'Cusick',
        'CWY':'Conway',
        'DAM':'Damman',
        'DAR':'Darrington',
        'DAVE':'Davenport',
        'DAYT':'Dayton',
        'DGR':'Dieringer',
        'DIXI':'Dixie',
        'DPRK':'Deer Park',
        'EAS':'Easton',
        'EAT':'Eatonville',
        'ED':'Edmonds',
        'ELM':'Elma',
        'ELN':'Ellensburg',
        'EMT':'Eastmont',
        'ENDI':'Endicott',
        'ENM':'Enumclaw',
        'ENT':'Entiat',
        'EPH':'Ephrata',
        'EV':'Everett',
        'EVA':'Evaline',
        'EVAL':'East Valley Spokane',
        'EVG':'Evergreen',
        'EVGR':'Evergreen - Hunters',
        'EYAK':'East Valley Yakima',
        'FED':'Federal Way',
        'FIF':'Fife',
        'FINL':'Finley',
        'FPS':'Franklin Pierce',
        'FREE':'Freeman',
        'FRN':'Ferndale',
        'GARF':'Garfield',
        'GF':'Granite Falls',
        'GLEN':'Glenwood',
        'GMT':'Green Mountain',
        'GOLD':'Goldendale',
        'GRC':'Grand Coulee',
        'GRF':'Griffin',
        'GRGR':'Granger',
        'GRNO':'Great Northern',
        'GRP':'Grapeview #54',
        'GRVW':'Grandview',
        'HARR':'Harrington',
        'HC':'Hood Canal #404',
        'HGL':'Highline',
        'HLND':'Highland',
        'HOC':'Hockinson',
        'HOQ':'Hoquiam',
        'INCH':'Inchelium',
        'IND':'Index',
        'ISS':'Issaquah',
        'KAHL':'Kahlotus',
        'KAL':'Kalama',
        'KEL':'Kelso',
        'KELR':'Keller',
        'KENN':'Kennewick',
        'KETF':'Kettle Falls',
        'KION':'Kiona-Benton City',
        'KLIC':'Klickitat',
        'KNT':'Kent',
        'KTS':'Kittitas',
        'LAC':'La Conner',
        'LACS':'Lacrosse',
        'LAMO':'Lamont',
        'LC':'La Center',
        'LCH':'Lake Chelan',
        'LGV':'Longview',
        'LIBR':'Liberty',
        'LIND':'Lind',
        'LKD':'Lakewood',
        'LKW':'Lake Washington',
        'LOON':'Loon Lake',
        'LPZ':'Lopez Island',
        'LS':'Lake Stevens',
        'LYLE':'Lyle',
        'LYN':'Lynden',
        'MABT':'Mabton',
        'MAR':'Marysville',
        'MARW':'Mary Walker',
        'MCC':'McCleary',
        'MEAD':'Mead',
        'MEDL':'Medical Lake',
        'MER':'Meridian',
        'MET':'Methow Valley',
        'MIS':'Mercer Island',
        'MK':'Mary M. Knight #311',
        'MLA':'Mill A',
        'MLK':'Moses Lake',
        'MNS':'Manson',
        'MON':'Monroe',
        'MOR':'Morton',
        'MOS':'Mossyrock',
        'MOT':'Montesano',
        'MSF':'Mansfield',
        'MTAD':'Mount Adams',
        'MTB':'Mount Baker',
        'MTP':'Mount Pleasant',
        'MTV':'Mount Vernon',
        'MUK':'Mukilteo',
        'NAP':'Napavine',
        'NAS':'Naselle-Grays River',
        'NAVY':'Naches Valley',
        'NBC':'North Beach',
        'NES':'Nespelem',
        'NEWP':'Newport',
        'NFRA':'North Franklin',
        'NK':'North Kitsap #400',
        'NM':'North Mason #403',
        'NMFS':'Nine Mile Falls',
        'NOO':'Nooksack Valley',
        'NPRT':'Northport',
        'NRV':'North River',
        'NTH':'Northshore',
        'NTN':'North Thurston',
        'OAK':'Oakville',
        'OAKS':'Oakesdale',
        'OCB':'Ocean Beach',
        'OCO':'Ocosta',
        'ODES':'Odessa',
        'OH':'Oak Harbor',
        'OKA':'Okanogan',
        'OLY':'Olympia',
        'OMA':'Omak',
        'ONA':'Onalaska',
        'ONCR':'Onion Creek',
        'ORC':'Orcas Island',
        'ORCH':'Orchard Prairie',
        'ORIE':'Orient',
        'ORO':'Orondo',
        'ORT':'Orting',
        'OTHE':'Othello',
        'OTHR':'Other',
        'OVL':'Oroville',
        'PAL':'Palisades',
        'PALO':'Palouse',
        'PASC':'Pasco',
        'PAT':'Pateros',
        'PATS':'Paterson',
        'PE':'Pe Ell',
        'PEN':'Peninsula',
        'PI':'Pioneer #402',
        'POME':'Pomeroy',
        'PRES':'Prescott',
        'PROS':'Prosser',
        'PTA':'Port Angeles',
        'PTT':'Port Townsend #50',
        'PULL':'Pullman',
        'PUY':'Puyallup',
        'QNC':'Quincy',
        'QTS':'Queets-Clearwater',
        'QUI':'Quinault',
        'QUL':'Quilcene',
        'QUT':'Quillayute',
        'RAI':'Rainier',
        'RAY':'Raymond',
        'REAR':'Reardan-Edwall',
        'REN':'Renton',
        'REPU':'Republic',
        'RICH':'Richland',
        'RID':'Ridgefield',
        'RITZ':'Ritzville',
        'ROC':'Rochester',
        'ROOS':'Roosevelt',
        'ROSA':'Rosalia',
        'RSID':'Riverside',
        'RVW':'Riverview',
        'RYL':'Royal',
        'SAN':'San Juan Island',
        'SAT':'Satsop',
        'SB':'South Bend',
        'SDW':'Sedro Woolley',
        'SEA':'Seattle',
        'SELA':'Selah',
        'SELK':'Selkirk',
        'SEQ':'Sequim',
        'SHL':'Shelton',
        'SHW':'Shaw Island',
        'SK':'South Kitsap',
        'SKM':'Skamania',
        'SKY':'Skykomish',
        'SNO':'Snohomish',
        'SPL':'Soap Lake',
        'SPOK':'Spokane',
        'SPRA':'Sprague',
        'SRI':'Shoreline',
        'SS':'South Side #42',
        'SSID':'Sunnyside',
        'ST':'Stanwood',
        'STAR':'Star',
        'STBU':'Starbuck',
        'STE':'Steilacoom Historica',
        'STEP':'Steptoe',
        'STH':'Stehekin',
        'STJO':'St. John',
        'STV':'Stevenson-Carson',
        'SUL':'Sultan',
        'SUM':'Sumner',
        'SUMM':'Summit Valley',
        'SVS':'Snoqualmie Valley',
        'SWI':'South Whidbey Island',
        'TAC':'Tacoma',
        'TEKO':'Tekoa',
        'TEN':'Tenino',
        'THL':'Taholah',
        'THO':'Thorp',
        'THS':'Tahoma',
        'TOL':'Toledo',
        'TOPP':'Toppenish',
        'TOU':'Toutle Lake',
        'TOUC':'Touchet',
        'TROU':'Trout Lake',
        'TSK':'Tonasket',
        'TUK':'Tukwila',
        'TUM':'Tumwater',
        'UGAP':'Union Gap',
        'UNP':'University Place',
        'VALY':'Valley',
        'VAN':'Vancouver',
        'VDR':'Vader',
        'VSH':'Vashon Island',
        'WAH':'Wahkiakum',
        'WAIT':'Waitsburg',
        'WAPA':'Wapato',
        'WAS':'Washougal',
        'WAWA':'Walla Walla',
        'WDL':'Woodland',
        'WELL':'Wellpinit',
        'WEN':'Wenatchee',
        'WHR':'White River',
        'WHT':'White Pass',
        'WILB':'Wilbur',
        'WIN':'Winlock',
        'WIS':'Wishkah',
        'WISH':'Wishram',
        'WLC':'Wilson Creek',
        'WLP':'Willapa',
        'WLU':'Wahluke',
        'WRD':'Warden',
        'WSAL':'White Salmon',
        'WTUC':'Washtucna',
        'WV':'Waterville',
        'WVAL':'West Valley Spokane',
        'WYAK':'West Valley Yakima',
        'YAKI':'Yakima',
        'YEL':'Yelm',
        'ZILA':'Zillah',
    }
}

@memoize
def _get_offices(username, password):
    for row in execute_listing_query(username, password, 'RetrieveOfficeData', {'MLS': 'nwmls'}):
        yield dict([(c.tag.replace('{http://www.nwmls.com/Schemas/Standard/StandardXML1_1.xsd}', ''), c.text) for c in row.getchildren()])


@memoize
def _get_amenities(username, password, prop_type):
    for r in execute_listing_query(username, password, 'RetrieveAmenityData', {'MLS': 'nwmls', 'PropertyType': prop_type}):
        field_name = r.find('{http://www.nwmls.com/Schemas/General/EverNetAmenityXML.xsd}Code').text
        values = r.find('{http://www.nwmls.com/Schemas/General/EverNetAmenityXML.xsd}Values').getchildren()
        row = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/General/EverNetAmenityXML.xsd}', ''), c.text) for c in values])
        yield field_name, row


def _get_office_table(offices):
    return dict([(office.get('{http://www.nwmls.com/Schemas/General/EverNetOfficeXML.xsd}OfficeMLSID'), office.get('{http://www.nwmls.com/Schemas/General/EverNetOfficeXML.xsd}OfficeName')) for office in offices])


def _get_amenities_table(amenities):
    field_map = defaultdict(dict)
    for field_name, row in amenities:
        field_map[field_name][row['Code']] = row['Description']
    return field_map


def _look_up_dynamic_fields(username, password, row):
    prop_type = row.get('PTYP')
    out = {}
    if not prop_type:
        return out
    lookup_table = _get_amenities_table(_get_amenities(username, password, prop_type))
    for key, value in row.items():
        if not value:
            continue
        if key not in lookup_table:
            out[key] = value
        else:
            out[key] = []
            for v in value.split('|'):
                out[key].append(lookup_table[key].get(v))
    return out

def _look_up_fixed_fields(row):
    out = {}
    for key, value in row.items():
        if key in FIXED_NWMLS_LOOKUPS:
            out[key] = FIXED_NWMLS_LOOKUPS[key].get(value, value)
        else:
            out[key] = value
    return out

def _add_office_name_fields(username, password, row):
    office_field_map = {
        'OFFICENAME': 'LO',
        'SELLINGOFFICENAME': 'SO',
    }

    offices = _get_office_table(_get_offices(username, password))

    for namefield, idfield in office_field_map.items():
        row[namefield] = offices.get(row.get(idfield))

    return row


def look_up_all_fields(username, password, row):
    row = _look_up_dynamic_fields(username, password, row)
    row = _add_office_name_fields(username, password, row)
    row = _look_up_fixed_fields(row)
    return row
