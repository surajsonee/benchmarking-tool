from .base import db
from .areas import *
from .packagedrtu import *
from .minisplitsystem import *
from .makeupairunit import *
from .infraredheater import *
from .windowairconditioner import *
from .condensingunitsystem import *
from .electricrestingheatingcoil import *
from .gasfiredheatingcoil import *
from .ahu import *
from .pipe import *
from .heat_pump import *
from .furnace import *
from .steam_boiler import *
from .motor import *
from .pump import *
from .chiller import *
from .commercialdhw import *
from .meters import *
from .light import *
from .foundation import *
from .rooffinish import *
from .roof import *
from .insulation import *
from .interiorwall import *
from .exteriorwall import *
from .commercialappliance import *
from .unitventilator import *
from .unitheater import *
from .selfcontainedahu import *
from .packagedterminalac import *

class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    city = db.Column(db.String(200), unique=False, nullable=False)
    province = db.Column(db.String(200), unique=False, nullable=False)
    postal_code = db.Column(db.String(200), unique=False, nullable=False)
    square_footage = db.Column(db.String(200), unique=False, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    areas = db.relationship('Area', backref='building')
    meters = db.relationship('Meter', backref='building')
    dhw = db.relationship('CommercialDHW', backref='building')
    chiller = db.relationship('Chiller', backref='building')
    pump = db.relationship('Pump', backref='buidling')
    motor = db.relationship('Motor', backref='building')
    steam_boiler = db.relationship('Steam_Boiler', backref='building')
    furnace = db.relationship('Furnace', backref='building')
    heat_pump = db.relationship('HeatPump', backref='building')
    pipe = db.relationship('Pipe', backref='building')
    ahu = db.relationship('AHU', backref='building')
    gasfiredheatingcoil = db.relationship('GasFiredHeatingCoil', backref='building')
    electricrestingheatingcoil = db.relationship('ElectricRestHeatingCoil', backref='building')
    condensingunitsystem = db.relationship('CondensingUnitSystem', backref='building')
    windowairconditioner = db.relationship('WindowAirConditioner', backref='building')
    infraredheater = db.relationship('InfraredHeater', backref='building')
    makeupairunit = db.relationship('MakeUpAirUnit', backref='building')
    minisplitsystem = db.relationship('MiniSplitSystem', backref='building')
    packagedrtu = db.relationship('PackagedRTU', backref='building')
    packagedterminalac = db.relationship('PackagedTerminalAC', backref='building')
    selfcontainedahu = db.relationship('SelfContainedAHU', backref='building')
    unitheater = db.relationship('UnitHeater', backref='building')
    unitventilator = db.relationship('UnitVentilator', backref='building')
    commercialappliance = db.relationship('CommercialAppliance', backref='building')
    exteriorwall = db.relationship('ExteriorWall', backref='building')
    interiorwall = db.relationship('InteriorWall', backref='building')
    insulation = db.relationship('Insulation', backref='building')
    roof = db.relationship('Roof', backref='building')
    rooffinish = db.relationship('RoofFinish', backref='building')
    foundation = db.relationship('Foundation', backref='building')
    light = db.relationship('Light', backref='building')
    photo_id = db.Column(db.String(300), unique=False, nullable=False)