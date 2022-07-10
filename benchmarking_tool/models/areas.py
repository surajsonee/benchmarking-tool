from .base import db
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
from .hydronic_boiler import *
class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    chillers = db.relationship('Chiller', backref='area')
    pumps = db.relationship('Pump', backref='area')
    motors = db.relationship('Motor', backref='area')
    hydronic_boilers = db.relationship('Hydronic_Boiler', backref='area')
    steam_boilers = db.relationship('Steam_Boiler', backref='area')
    furnaces = db.relationship('Furnace', backref='area')
    heat_pumps = db.relationship('HeatPump', backref='area')
    pipes = db.relationship('Pipe', backref='area')
    vav_ahu = db.relationship('AHU', backref='area')
    gas_fired_heating_coil = db.relationship('GasFiredHeatingCoil', backref='area')
    electric_rest_heating_coil = db.relationship('ElectricRestHeatingCoil', backref='area')
    condensing_unit_system = db.relationship('CondensingUnitSystem', backref='area')
    infrared_heater = db.relationship('InfraredHeater', backref='area')
    make_up_air_units = db.relationship('MakeUpAirUnit', backref='area')
    mini_split_system = db.relationship('MiniSplitSystem', backref='area')
    packaged_rtu = db.relationship('PackagedRTU', backref='area')
    packaged_terminal_ac = db.relationship('PackagedTerminalAC', backref='area')
    self_contained_ahu = db.relationship('SelfContainedAHU', backref='area')
    unit_heater = db.relationship('UnitHeater', backref='area')
    unit_ventilator = db.relationship('UnitVentilator', backref='area')
    window_air_conditioner = db.relationship('WindowAirConditioner', backref='area')

    lights = db.relationship('Light', backref='area')
    dhws = db.relationship('CommercialDHW', backref='area')
    commercialappliances = db.relationship('CommercialAppliance', backref='area')
    interiorwall = db.relationship('InteriorWall', backref='area')
    photo_id1 = db.Column(db.String(300), unique=False, nullable=False)
    photo_id2 = db.Column(db.String(300), unique=False, nullable=False)

