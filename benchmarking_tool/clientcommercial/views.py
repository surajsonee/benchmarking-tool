from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import flask_excel as excel
import pandas as pd
import os
from werkzeug.utils import secure_filename
import json
from sqlalchemy.orm import load_only
import time
import hashlib

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, FileField, SelectField, IntegerField


#docx templating shit
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage

from flask import Flask, send_file




from docx import Document
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    from io import BytesIO
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage



from docx import Document
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    from io import BytesIO
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage


import math
from sqlalchemy import desc
from flask import Blueprint,render_template,request,redirect,url_for,flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from ..models import *
from pathlib import Path
import requests
from benchmarking_tool.helper import *
from benchmarking_tool.forms import *
from benchmarking_tool.decorators import *
from benchmarking_tool.functions import *
import secrets
from PIL import Image
from difflib import get_close_matches
from benchmarking_tool.furnace_detect import *
from benchmarking_tool.pvc_steel_detect import *
from benchmarking_tool.image_reckognition.aws_rek import *
from benchmarking_tool.image_reckognition.bill_detection import *
from benchmarking_tool.methods import *
from datetime import datetime,timedelta
from sqlalchemy import and_
from sqlalchemy.sql.expression import func
from flask_mobility.decorators import mobile_template, mobilized
from flask import session
import csv
import operator
import boto3
import sys
import os
import pandas as pd
from flask_mail import Mail, Message
#for photo upload
# basedir = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# excel.init_excel(app)


# app.config['SECRET_KEY'] = 'I have a dream'
# app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads') # you'll need to create a folder named uploads

# configure_uploads(app, photos)
# patch_request_class(app)  # set maximum file size, default is 16MB

clientcommercial = Blueprint('clientcommercial',__name__,template_folder='templates', url_prefix='/clientcommercial')
app_root = Path(__file__).parents[1]

@clientcommercial.route('/buildinglist', methods =['GET', 'POST'])
@login_required
def buildinglist():
    if(current_user.is_authenticated and current_user.is_client()):
        clients = Client.query.order_by(Client.created_at).all()
        buildings = Building.query.order_by(Building.client_id).all()
        return render_template('buildinglist.html', clients=clients, buildings = buildings)
    else:
        abort(403)

@clientcommercial.route('/arealist', methods =['GET', 'POST'])
@login_required
def arealist():
    if(current_user.is_authenticated and current_user.is_client()):
        buildings = Building.query.order_by(Building.client_id).all()
        areas = Area.query.order_by(Area.building_id).all()
        return render_template('arealist.html', areas=areas, buildings = buildings)
    else:
        abort(403)

@clientcommercial.route('/buildingindex', methods=['GET', 'POST'])
@login_required
def buildingindex():
    if(current_user.is_authenticated and current_user.is_client()):
        customer = Customer.query.filter_by(user_id=current_user.id).first()
        client = Client.query.filter_by(customer_id=customer.id).first()
        building_id = client.id
        buildings = Building.query.filter_by(client_id=building_id).all()
        return render_template('buildingindex.html', client=client, buildings=buildings)
    else:
        abort(403)

@clientcommercial.route('/addbuilding/<int:id>', methods=['GET', 'POST'])
@login_required
def addbuilding(id):
    if(current_user.is_authenticated and current_user.is_client()):
        client = Client.query.get(id)
        form = BuildingForm()
        if request.method == 'POST':
            building_name = request.form["building_name"]
            address = request.form["address"]
            city = request.form["city"]
            province = request.form["province"]
            postal_code = request.form["postal_code"]
            square_footage = request.form["square_footage"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            new_building = Building(photo=photo,name=building_name, address=address, city=city, province=province,
                                    postal_code=postal_code, square_footage=square_footage, owner=client)
            try:
                db.session.add(new_building)
                db.session.commit()
                building_id = id
                buildings = Building.query.filter_by(client_id=building_id).all()
                return redirect('/buildingindex/' + str(id))
            except:
                return "There was an error adding building"
        else:
            return render_template('addbuilding.html', client=client,form=form)
    else:
        abort(403)

@clientcommercial.route('/addbuilding/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updatebuilding(id):
    if(current_user.is_authenticated and current_user.is_client()):
        building = Building.query.get_or_404(id)
        client = building.client_id
        form = BuildingForm()
        if form.validate_on_submit():
            building.name = form.building_name.data
            building.address = form.address.data
            building.city = form.city.data 
            building.province = form.province.data 
            building.postal_code = form.postal_code.data 
            building.square_footage = form.square_footage.data 
            db.session.commit()
            return redirect(url_for('commercial.buildingindex', client = client, id = client))

        elif request.method == 'GET':
            form.building_name.data = building.name
            form.address.data = building.address
            form.city.data = building.city
            form.province.data = building.province
            form.postal_code.data = building.postal_code
            form.square_footage.data = building.square_footage
        return render_template('addbuilding.html', form = form, client = client)
    else:
        abort(403)


@clientcommercial.route('/addbuilding/<int:id>/delete', methods=['POST'])
@login_required
def deletebuilding(id):
    if(current_user.is_authenticated and current_user.is_client()):
        buidling = Building.query.get_or_404(id)
        area = buidling.client_id
        db.session.delete(buidling)
        db.session.commit()
        return redirect(url_for('commercial.buildingindex',area = area, id = area))
    else:
        abort(403)

@clientcommercial.route('/utilityindex/<int:id>', methods=['GET', 'POST'])
@login_required
def utilityindex(id):
    if(current_user.is_authenticated and current_user.is_client()):
        building = Building.query.get(id)
        meter_id = id
        meters = Meter.query.filter_by(building_id=meter_id).all()
        return render_template('utility_index.html', building=building, meters=meters)
    else:
        abort(403)

@clientcommercial.route('/utilityinfoupload/<int:id>', methods=['GET', 'POST'])
@login_required
def utilityupload(id):
    if(current_user.is_authenticated and current_user.is_client()):
        building = Building.query.get(id)
        meter_id = id
        meters = Meter.query.filter_by(building_id=meter_id).all()
        if request.method == 'POST':
            distributer = request.form["distributer"]
            meter_number = request.form["meter_number"]
            account_number = request.form["account_number"]
            energy_type = request.form["energy_type"]
            new_meter = Meter(distributer=distributer, meter_number=meter_number,
                              account_number=account_number, energy_type=energy_type, building=building)
            db.session.add(new_meter)
            db.session.commit()
            return redirect('/utilityindex/'+str(id))
            # except:
            # return "There was an error adding meter"
        else:
            return render_template("add_meter.html", building=building, meters=meters)
    else:
        abort(403)

@clientcommercial.route('/constructionindex/<int:id>', methods=['GET', 'POST'])
@login_required
def construction(id):
    if(current_user.is_authenticated and current_user.is_client()):
        building = Building.query.get(id)
        construction_id = id
        exteriorwalls = ExteriorWall.query.filter_by(building_id=construction_id).all()
        foundations = Foundation.query.filter_by(building_id=construction_id).all()
        roofs = Roof.query.filter_by(building_id=construction_id).all()
        rooffinishs = RoofFinish.query.filter_by(building_id=construction_id).all()
        return render_template('constructionindex.html', building=building.id, building_id = id, exteriorwalls=exteriorwalls, foundations=foundations,roofs=roofs,rooffinishs = rooffinishs)
    else:
        abort(403)
@clientcommercial.route('/addexteriorwall/<int:id>', methods=['GET', 'POST'])
@login_required
def addexteriorwall(id): 
    if(current_user.is_authenticated and current_user.is_client()):
        building = Building.query.get(id)
        exteriorwall_id = id
        exteriorwalls = ExteriorWall.query.filter_by(building_id=exteriorwall_id).all()
        form = ExteriorWallForm()

        if request.method == 'POST':
            material = request.form["material"]
            rvalue = request.form["rvalue"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            new_exteriorwall = ExteriorWall(photo=photo,material=material, rvalue=rvalue, building_id = building.id)
            db.session.add(new_exteriorwall)
            db.session.commit()
            return redirect('/constructionindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('addexteriorwall.html', building=building, exteriorwalls=exteriorwalls,form=form)
    else:
        abort(403)
@clientcommercial.route('/addroof/<int:id>', methods=['GET', 'POST'])
@login_required
def addroof(id): 
    if(current_user.is_authenticated and current_user.is_client()):
        building = Building.query.get(id)
        roof_id = id
        roofs = Roof.query.filter_by(building_id=roof_id).all()
        form = RoofForm()

        if request.method == 'POST':
            material = request.form["material"]
            rvalue = request.form["rvalue"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            new_roof = Roof(photo=photo,material=material, rvalue=rvalue, building_id = building.id)
            db.session.add(new_roof)
            db.session.commit()
            return redirect('/constructionindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('addroof.html', building=building, roofs=roofs,form=form)
    else:
        abort(403)
@clientcommercial.route('/addrooffinish/<int:id>', methods=['GET', 'POST'])
@login_required
def addrooffinish(id): 
    if(current_user.is_authenticated and current_user.is_client()):
        building = Building.query.get(id)
        rooffinish_id = id
        rooffinishs = RoofFinish.query.filter_by(building_id=rooffinish_id).all()
        form = RoofFinishForm()

        if request.method == 'POST':
            material = request.form["material"]
            rvalue = request.form["rvalue"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            new_rooffinish = RoofFinish(photo=photo,material=material, rvalue=rvalue, building_id = building.id)
            db.session.add(new_rooffinish)
            db.session.commit()
            return redirect('/constructionindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('addrooffinish.html', building=building, rooffinishs=rooffinishs,form=form)
    else:
        abort(403)
@clientcommercial.route('/addfoundation/<int:id>', methods=['GET', 'POST'])
@login_required
def addfoundation(id): 
    if(current_user.is_authenticated and current_user.is_client()):
        building = Building.query.get(id)
        foundation_id = id
        foundations = Foundation.query.filter_by(building_id=foundation_id).all()
        form = FoundationForm()

        if request.method == 'POST':
            foundation_type = request.form["foundation_type"]
            material = request.form["material"]
            rx = request.form["rx"]
            rvalue = request.form["rvalue"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            new_foundation = Foundation(photo=photo,material=material, rvalue=rvalue, foundationtype = foundation_type, rx=rx, building_id = building.id)
            db.session.add(new_foundation)
            db.session.commit()
            return redirect('/constructionindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('addfoundation.html', building=building, foundations=foundations,form=form)
    else:
        abort(403)


@clientcommercial.route('/areaindex/<int:id>', methods=['GET', 'POST'])
@login_required
def areas(id):
    if(current_user.is_authenticated and current_user.is_client()):
        building = Building.query.get(id)
        area_id = id
        areas = Area.query.filter_by(building_id=area_id).all()
        if request.method == 'POST':
            name = request.form['name']
            new_room = Area(name=name, building=building)
            try:
                db.session.add(new_room)
                db.session.commit()
                building = Building.query.get(id)
                area_id = id
                areas = Area.query.filter_by(building_id=area_id)
                return redirect('/areaindex/'+str(id))
            except:
                "There was an error adding area"
        else:
            return render_template('area_index.html', building=building, areas=areas)
    else:
        abort(403)
@clientcommercial.route('/updatearea/<int:id>', methods=['GET', 'POST'])
@login_required
def updatearea(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = AreaForm()
        if form.validate_on_submit():
            area.name = form.name.data
            db.session.commit()
            return redirect(url_for('commercial.areas', building = building, id = building))

        elif request.method == 'GET':
            form.name.data = area.name
        return render_template('update_area.html', form = form, building = building)
    else:
        abort(403)


@clientcommercial.route('/areaindex/<int:id>/delete', methods=['POST'])
@login_required
def deletearea(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area_obj = Area.query.get_or_404(id)
        area = area_obj.building_id
        db.session.delete(area_obj)
        db.session.commit()
        return redirect(url_for('commercial.areas',area = area, id = area))
    else:
        abort(403)  

@clientcommercial.route('/lightindex/<int:id>', methods=['GET', 'POST'])
@login_required
def lightindex(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        light_id = id
        lights = Light.query.filter_by(area_id=light_id).all()
        return render_template('lightindex.html', area=area, lights=lights)
    else:
        abort(403)

@clientcommercial.route('/addlight/<int:id>', methods=['GET', 'POST'])
@login_required
def lights(id):
    if(current_user.is_authenticated and current_user.is_client()):

        area = Area.query.get(id)
        building = area.building_id
        light_id = id
        lights = Light.query.filter_by(area_id=light_id).all()
        form = LightForm()

        if request.method == 'POST':
            fixture_count = request.form["fixtures"]
            hours = request.form["hours"]
            fixture = request.form["fixture_type"]
            lamp = request.form["lamp_type"]
            wattage = request.form["wattage"]
            lamp_count = request.form["lamp_count"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            new_light = Light(photo=photo,fixture_count=fixture_count, hours=hours, fixture=fixture, lamp=lamp,
                              wattage=wattage, lamp_count=lamp_count, area = area, building_id = building)
            db.session.add(new_light)
            db.session.commit()
            return redirect('/lightindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('addlight.html', area=area, lights=lights,form=form)
    else:
        abort(403)
@clientcommercial.route('/duplicatelight/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatelight(id):
    if(current_user.is_authenticated and current_user.is_client()):
        light_id = id
        light = Light.query.get(id)
        form = LightForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_light = Light(photo=light.photo,fixture_count=light.fixture_count, hours=light.hours, fixture=light.fixture, lamp=light.lamp,
                              wattage=light.wattage, lamp_count=light.lamp_count, area = light.area, building_id = light.building_id)
            db.session.add(new_light)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.lightindex', id = light.area_id))
    else:
        abort(403)
@clientcommercial.route('/addlight/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updatelight(id):
    if(current_user.is_authenticated and current_user.is_client()):
        light = Light.query.get(id)
        area = light.area_id
        form = LightForm()
        if form.validate_on_submit():
            light.fixture_count = form.fixtures.data
            light.hours = form.hours.data
            light.fixture = form.fixture_type.data 
            light.lamp = form.lamp_type.data 
            light.wattage = form.wattage.data 
            light.lamp_count = form.lamp_count.data 
            db.session.commit()
            return redirect(url_for('commercial.lightindex', area = area, id = area))

        elif request.method == 'GET':
            form.fixtures.data = light.fixture_count
            form.hours.data = light.hours
            form.fixture_type.data = light.fixture
            form.lamp_type.data = light.lamp
            form.wattage.data = light.wattage
            form.lamp_count.data = light.lamp_count
        return render_template('addlight.html', form = form, area = area)
    else:
        abort(403)
@clientcommercial.route('/addlight/<int:id>/delete', methods=['POST'])
@login_required
def deletelight(id):
    if(current_user.is_authenticated and current_user.is_client()):
        light = Light.query.get_or_404(id)
        area = light.area_id
        db.session.delete(light)
        db.session.commit()
        return redirect(url_for('commercial.lightindex',area = area, id = area))
    else:
        abort(403)

@clientcommercial.route('/equipmentindex/<int:id>', methods=['GET', 'POST'])
@login_required
def equipmentindex(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        area_id = id
        furnaces = Furnace.query.filter_by(area_id=area_id).all()
        chillers = Chiller.query.filter_by(area_id=area_id).all()
        pumps = Pump.query.filter_by(area_id=area_id).all()
        motors = Motor.query.filter_by(area_id=area_id).all()
        hydronic_boilers = Hydronic_Boiler.query.filter_by(area_id=area_id).all()
        steam_boilers = Steam_Boiler.query.filter_by(area_id=area_id).all()
        heat_pumps = HeatPump.query.filter_by(area_id=area_id).all()
        ahus = AHU.query.filter_by(area_id=area_id).all()
        gas_fired_heating_coils = GasFiredHeatingCoil.query.filter_by(area_id=area_id).all()
        electric_rest_heating_coils = ElectricRestHeatingCoil.query.filter_by(area_id=area_id).all()
        condensing_unit_systems = CondensingUnitSystem.query.filter_by(area_id=area_id).all()
        window_air_conditioners = WindowAirConditioner.query.filter_by(area_id=area_id).all()

        infrared_heaters = InfraredHeater.query.filter_by(area_id=area_id).all()
        make_up_air_units = MakeUpAirUnit.query.filter_by(area_id=area_id).all()
        mini_split_systems = MiniSplitSystem.query.filter_by(area_id=area_id).all()
        packaged_rtus = PackagedRTU.query.filter_by(area_id=area_id).all()
        packaged_terminal_acs = PackagedTerminalAC.query.filter_by(area_id=area_id).all()
        self_contained_ahus = SelfContainedAHU.query.filter_by(area_id=area_id).all()
        unit_heaters = UnitHeater.query.filter_by(area_id=area_id).all()
        unit_ventilators = UnitVentilator.query.filter_by(area_id=area_id).all()
        dhws = DHW.query.filter_by(area_id=area_id).all()
        appliances = Appliance.query.filter_by(area_id=area_id).all()
        return render_template('equipmentindex.html', area=area, dhws=dhws, appliances=appliances,furnaces=furnaces,chillers=chillers,pumps=pumps,motors=motors,hydronic_boilers=hydronic_boilers,steam_boilers=steam_boilers,
            heat_pumps=heat_pumps,window_air_conditioners=window_air_conditioners,ahus=ahus,gas_fired_heating_coils=gas_fired_heating_coils,electric_rest_heating_coils=electric_rest_heating_coils,condensing_unit_systems=condensing_unit_systems,
            infrared_heaters= infrared_heaters,make_up_air_units=make_up_air_units,mini_split_systems=mini_split_systems,packaged_rtus=packaged_rtus,packaged_terminal_acs=packaged_terminal_acs,
            self_contained_ahus=self_contained_ahus,unit_heaters=unit_heaters,unit_ventilators=unit_ventilators)
    else:
        abort(403)

@clientcommercial.route('/hvac_index/<int:id>', methods=['GET', 'POST'])
@login_required
def hvac(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        area_id = id
        furnaces = Furnace.query.filter_by(area_id=area_id).all()
        chillers = Chiller.query.filter_by(area_id=area_id).all()
        pumps = Pump.query.filter_by(area_id=area_id).all()
        motors = Motor.query.filter_by(area_id=area_id).all()
        hydronic_boilers = Hydronic_Boiler.query.filter_by(area_id=area_id).all()
        steam_boilers = Steam_Boiler.query.filter_by(area_id=area_id).all()
        heat_pumps = HeatPump.query.filter_by(area_id=area_id).all()
        ahus = AHU.query.filter_by(area_id=area_id).all()
        gas_fired_heating_coils = GasFiredHeatingCoil.query.filter_by(area_id=area_id).all()
        electric_rest_heating_coils = ElectricRestHeatingCoil.query.filter_by(area_id=area_id).all()
        condensing_unit_systems = CondensingUnitSystem.query.filter_by(area_id=area_id).all()
        window_air_conditioners = WindowAirConditioner.query.filter_by(area_id=area_id).all()

        infrared_heaters = InfraredHeater.query.filter_by(area_id=area_id).all()
        make_up_air_units = MakeUpAirUnit.query.filter_by(area_id=area_id).all()
        mini_split_systems = MiniSplitSystem.query.filter_by(area_id=area_id).all()
        packaged_rtus = PackagedRTU.query.filter_by(area_id=area_id).all()
        packaged_terminal_acs = PackagedTerminalAC.query.filter_by(area_id=area_id).all()
        self_contained_ahus = SelfContainedAHU.query.filter_by(area_id=area_id).all()
        unit_heaters = UnitHeater.query.filter_by(area_id=area_id).all()
        unit_ventilators = UnitVentilator.query.filter_by(area_id=area_id).all()
        return render_template('hvac_index.html',area=area, furnaces=furnaces,chillers=chillers,pumps=pumps,motors=motors,hydronic_boilers=hydronic_boilers,steam_boilers=steam_boilers,
            heat_pumps=heat_pumps,window_air_conditioners=window_air_conditioners,ahus=ahus,gas_fired_heating_coils=gas_fired_heating_coils,electric_rest_heating_coils=electric_rest_heating_coils,condensing_unit_systems=condensing_unit_systems,
            infrared_heaters= infrared_heaters,make_up_air_units=make_up_air_units,mini_split_systems=mini_split_systems,packaged_rtus=packaged_rtus,packaged_terminal_acs=packaged_terminal_acs,
            self_contained_ahus=self_contained_ahus,unit_heaters=unit_heaters,unit_ventilators=unit_ventilators)
    else:
        abort(403)


@clientcommercial.route('/adddhw/<int:id>', methods=['GET', 'POST'])
@login_required
def dhw(id):
    if(current_user.is_authenticated and current_user.is_client()):

        area = Area.query.get(id)
        building = area.building_id
        dhw_id = id
        dhws = DHW.query.filter_by(area_id=dhw_id).all()
        form = DHWForm()

        if request.method == 'POST':
            equipment_type = request.form["equipment_type"]
            tag = request.form["tag"]
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            input_capacity = request.form["input_capacity"]
            fuel_type = request.form["fuel_type"]
            efficiency = request.form["efficiency"]
            storage_volume = request.form["storage_volume"]
            set_point = request.form["set_point"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            new_dhw = DHW(photo=photo, equipment_type=equipment_type, tag=tag, manufacturer=manufacturer, model_number=model_number,
                          serial_number=serial_number, input_capacity=input_capacity, fuel_type=fuel_type, efficiency=efficiency, storage_volume=storage_volume, set_point=set_point, area=area,building_id = building)
            db.session.add(new_dhw)
            db.session.commit()
            return redirect('/equipmentindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('add_dhw_equipment.html', area=area, dhws=dhws, form=form)
    else:
        abort(403)

@clientcommercial.route('/adddhw/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updatedhw(id):
    if(current_user.is_authenticated and current_user.is_client()):
        dhw = DHW.query.get(id)
        area = dhw.area_id
        form = DHWForm()
        if form.validate_on_submit():
            dhw.equipment_type = form.equipment_type.data
            dhw.tag = form.tag.data
            dhw.manufacturer = form.manufacturer.data
            dhw.model_number = form.model_number.data
            dhw.serial_number = form.serial_number.data 
            dhw.input_capacity = form.input_capacity.data 
            dhw.fuel_type = form.fuel_type.data 
            dhw.efficiency = form.efficiency.data 
            dhw.storage_volume = form.storage_volume.data 
            dhw.set_point = form.set_point.data 
            db.session.commit()
            return redirect(url_for('commercial.equipmentindex', area = area, id = area))

        elif request.method == 'GET':
            form.equipment_type.data = dhw.equipment_type
            form.tag.data = dhw.tag
            form.manufacturer.data = dhw.manufacturer
            form.model_number.data = dhw.model_number
            form.input_capacity.data = dhw.input_capacity
            form.fuel_type.data = dhw.fuel_type
            form.efficiency.data = dhw.efficiency
            form.storage_volume.data = dhw.storage_volume
            form.set_point.data = dhw.set_point
            form.set_point.data = dhw.set_point

        return render_template('add_dhw_equipment.html', form = form, area = area)
    else:
        abort(403)

@clientcommercial.route('/adddhw/<int:id>/delete', methods=['POST'])
@login_required
def deletedhw(id):
    if(current_user.is_authenticated and current_user.is_client()):
        dhw = DHW.query.get_or_404(id)
        area = dhw.area_id
        db.session.delete(dhw)
        db.session.commit()
        return redirect(url_for('commercial.equipmentindex',area = area, id = area))
    else:
        abort(403)

@clientcommercial.route('/duplicatedhw/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatedhw(id):
    if(current_user.is_authenticated and current_user.is_client()):
        dhw_id = id
        dhw = DHW.query.get(id)
        form = DHWForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_dhw = DHW(photo=dhw.photo, equipment_type=dhw.equipment_type, tag=dhw.tag, manufacturer=dhw.manufacturer, model_number=dhw.model_number,
                          serial_number=dhw.serial_number, input_capacity=dhw.input_capacity, fuel_type=dhw.fuel_type, efficiency=dhw.efficiency, storage_volume=dhw.storage_volume, set_point=dhw.set_point, area=dhw.area,building_id = dhw.building)
            db.session.add(new_dhw)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = dhw.area_id))
    else:
        abort(403)

@clientcommercial.route('/addappliance/<int:id>', methods=['GET', 'POST'])
@login_required
def appliance(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        appliance_id = id
        appliances = Appliance.query.filter_by(area_id=appliance_id).all()
        form = ApplianceForm()

        if request.method == 'POST':
            appliance_type = request.form["appliance_type"]
            quantity = request.form["quantity"]
            wattage = request.form["wattage"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            new_appliance = Appliance(photo=photo,
                appliance_type=appliance_type, quantity=quantity, wattage=wattage, area=area, building_id = building)
            db.session.add(new_appliance)
            db.session.commit()
            return redirect('/equipmentindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('add_appliance_equipment.html', area=area, appliances=appliances, form=form)
    else:
        abort(403)
@clientcommercial.route('/addappliance/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updateappliance(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        appliance = Appliance.query.get_or_404(id)
        form = ApplianceForm()
        if form.validate_on_submit():
           appliance.appliance_type = form.appliance_type.data
           appliance.quantity = form.quantity.data
           appliance.wattage = form.wattage.data 
           db.session.commit()
           return redirect('/equipmentindex/'+str(id))

        elif request.method == 'GET':
            form.appliance_type.data = appliance.appliance_type   
            form.quantity.data = appliance.quantity
            form.wattage.data = appliance.wattage 
            form.photo.data = appliance.photo
        return render_template('add_appliance_equipment.html', form = form, area = area, appliance = appliance)
    else:
        abort(403)
@clientcommercial.route('/addappliance/<int:id>/delete', methods=['POST'])
@login_required
def deleteappliance(id):
    if(current_user.is_authenticated and current_user.is_client()):
        appliance = Appliance.query.get_or_404(id)
        area = appliance.area_id
        db.session.delete(appliance)
        db.session.commit()
        return redirect(url_for('commercial.equipmentindex',area = area, id = area))
    else:
        abort(403)

@clientcommercial.route('/duplicateappliance/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateappliance(id):
    if(current_user.is_authenticated and current_user.is_client()):
        appliance_id = id
        appliance = Appliance.query.get(id)
        form = ApplianceForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_appliance = Appliance(photo=appliance.photo,
                appliance_type=appliance.appliance_type, quantity=appliance.quantity, wattage=appliance.wattage, building_id = appliance.building,
                          serial_number=appliance.serial_number, input_capacity=appliance.input_capacity, fuel_type=appliance.fuel_type, efficiency=appliance.efficiency, storage_volume=appliance.storage_volume, set_point=appliance.set_point, area=appliance.area)
            db.session.add(new_appliance)
            db.session.commit()
            loop += 1
        return redirect(url_for('commercial.equipmentindex', id = appliance.area_id))
    else:
        abort(403)


@clientcommercial.route('/uploadbills/<int:id>', methods=['GET', 'POST'])
@login_required
def uploadbills(id):
    if(current_user.is_authenticated and current_user.is_client()):
        meter = Meter.query.get(id)
        meter_number = meter.meter_number
        bill_id=id
        bills = Utility_Bill.query.filter_by(meter_number=meter_number).all()

        if request.method == 'POST':

            def Utility_Bill_init_func(row):
                p = Utility_Bill(row['start_date'],
                                 row['end_date'], row['usage'], row['cost'], meter_number)
                return p

            request.save_to_database(
                field_name='file', session=db.session,
                table=Utility_Bill,
                initializer=Utility_Bill_init_func)

            return redirect('/billindex/'+ str(id))

        return render_template('utility_uploader.html', meter=meter, bills=bills)
    else:
        abort(403)





@clientcommercial.route("/billindex/<int:id>", methods=['GET', 'POST'])
@login_required
def bill(id):
    if(current_user.is_authenticated and current_user.is_client()):
        meter = Meter.query.get(id)
        meter_number = meter.meter_number
        bill_id=id
        bills = Utility_Bill.query.filter_by(meter_number=meter_number).all()
        def Utility_Bill_init_func(row):
            p = Utility_bill(row['start_date'],
                         row['end_date'], row['usage'], row['cost'], meter_number)
            bills=p.query.filter_by(meter_number=meter_number).all()
    #try swapping def
            return excel.make_response_from_tables(db.session, [p], 'handsontable.html')
        return ""
    else:
        abort(403)


@clientcommercial.route("/add_steam_boiler/<int:id>", methods=['GET', 'POST'])
@login_required
def add_steam_boiler(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        form = SteamBoilerForm()
        building = area.building_id

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            heating_eff = request.form['heating_eff']
            boiler_type = request.form["boiler_type"]
            pressure = request.form["pressure"]
            area_id = id
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            steam_boiler = Steam_Boiler(building_id = building, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=heating_eff,boiler_type=boiler_type,pressure=pressure,area=area,photo=photo)
            db.session.add(steam_boiler)
            db.session.commit()
            return redirect('/hvac_index/'+str(id))

        else:
            return render_template('add_hvac_equipment.html', add='steam_boiler',area=area,form=form)
    else:
        abort(403)


@clientcommercial.route("/add_steam_boiler/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_steam_boiler(id):
    if(current_user.is_authenticated and current_user.is_client()):
        steam_boiler = Steam_Boiler.query.get_or_404(id)
        area = steam_boiler.area_id
        form = SteamBoilerForm()
        if form.validate_on_submit():
           steam_boiler.manufacturer = form.manufacturer.data
           steam_boiler.model_number = form.model_number.data
           steam_boiler.serial_number = form.serial_number.data 
           steam_boiler.year_built = form.year_built.data
           steam_boiler.input_capacity = form.input_capacity.data
           steam_boiler.output_capacity = form.output_capacity.data 
           steam_boiler.effciency = form.heating_eff.data
           steam_boiler.boiler_type = form.boiler_type.data
           steam_boiler.pressure = form.pressure.data 
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = steam_boiler.manufacturer   
            form.model_number.data = steam_boiler.model_number
            form.serial_number.data = steam_boiler.serial_number 
            form.year_built.data = steam_boiler.year_built
            form.input_capacity.data = steam_boiler.input_capacity   
            form.output_capacity.data = steam_boiler.output_capacity
            form.heating_eff.data = steam_boiler.effciency 
            form.boiler_type.data = steam_boiler.boiler_type   
            form.pressure.data = steam_boiler.pressure
        return render_template('add_hvac_equipment.html', add='steam_boiler',area=area,form=form)
    else:
        abort(403)

@clientcommercial.route('/add_steam_boiler/<int:id>/delete', methods=['POST'])
@login_required
def deletesteamboiler(id):
    if(current_user.is_authenticated and current_user.is_client()):
        steam_boiler = Steam_Boiler.query.get_or_404(id)
        area = steam_boiler.area_id
        db.session.delete(steam_boiler)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@clientcommercial.route('/duplicatesteamboiler/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatesteamboiler(id):
    if(current_user.is_authenticated and current_user.is_client()):
        steamboiler_id = id
        steamboiler = Steam_Boiler.query.get(id)
        form = SteamBoilerForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            steam_boiler = Steam_Boiler(building_id = steamboiler.building, manufacturer=steamboiler.manufacturer,model_number=steamboiler.model_number,serial_number=steamboiler.serial_number,year_built=steamboiler.year_built,input_capacity=steamboiler.input_capacity,output_capacity=steamboiler.output_capacity,effciency=steamboiler.heating_eff,boiler_type=steamboiler.boiler_type,pressure=steamboiler.pressure,area=steamboiler.area,photo=steamboiler.photo)
            db.session.add(steam_boiler)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.hvacindex', id = steamboiler.area_id))
    else:
        abort(403)

@clientcommercial.route("/add_hydronic_boiler/<int:id>", methods=['GET', 'POST'])
@login_required
def add_hydronic_boiler(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = HydronicBoilerForm()
        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            heating_eff = request.form['heating_eff']
            type_boiler = request.form["boiler_type"]
            lhwt = request.form["lhwt"]
            ehwt = request.form['ehwt']
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            hydronic_boiler = Hydronic_Boiler(building_id = building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=heating_eff,boiler_type=type_boiler,lhwt=lhwt,ehwt=ehwt,area=area)
            try:
                db.session.add(hydronic_boiler)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding boiler"
        else:
            return render_template('add_hvac_equipment.html', add='hydronic_boiler',area=area, form=form)
    else:
        abort(403)

@clientcommercial.route("/add_hydronic_boiler/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_hydronic_boiler(id):
    if(current_user.is_authenticated and current_user.is_client()):
        hydronic_boiler = Hydronic_Boiler.query.get_or_404(id)
        area = hydronic_boiler.area_id
        form = HydronicBoilerForm()
        if form.validate_on_submit():
           hydronic_boiler.manufacturer = form.manufacturer.data
           hydronic_boiler.model_number = form.model_number.data
           hydronic_boiler.serial_number = form.serial_number.data 
           hydronic_boiler.year_built = form.year_built.data
           hydronic_boiler.input_capacity = form.input_capacity.data
           hydronic_boiler.output_capacity = form.output_capacity.data 
           hydronic_boiler.effciency = form.heating_eff.data
           hydronic_boiler.boiler_type = form.boiler_type.data
           hydronic_boiler.lhwt = form.lhwt.data
           hydronic_boiler.ehwt = form.ehwt.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = hydronic_boiler.manufacturer   
            form.model_number.data = hydronic_boiler.model_number
            form.serial_number.data = hydronic_boiler.serial_number 
            form.year_built.data = hydronic_boiler.year_built
            form.input_capacity.data = hydronic_boiler.input_capacity   
            form.output_capacity.data = hydronic_boiler.output_capacity
            form.heating_eff.data = hydronic_boiler.effciency 
            form.boiler_type.data = hydronic_boiler.boiler_type   
            form.lhwt.data = hydronic_boiler.lhwt
            form.ehwt.data = hydronic_boiler.ehwt
        return render_template('add_hvac_equipment.html', add='hydronic_boiler',area=area,form=form)
    else:
        abort(403)


@clientcommercial.route('/add_hydronic_boiler/<int:id>/delete', methods=['POST'])
@login_required
def deletehydronicboiler(id):
    if(current_user.is_authenticated and current_user.is_client()):
        hydronic_boiler = Hydronic_Boiler.query.get_or_404(id)
        area = hydronic_boiler.area_id
        db.session.delete(hydronic_boiler)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@clientcommercial.route('/duplicatehydronicboiler/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatehydronicboiler(id):
    if(current_user.is_authenticated and current_user.is_client()):

        hydronicboiler_id = id
        hydronicboiler = Hydronic_Boiler.query.get(id)
        form = HydronicBoilerForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            hydronic_boiler = Hydronic_Boiler(building_id = hydronicboiler.building,photo=hydronicboiler.photo, manufacturer=hydronicboiler.manufacturer,model_number=hydronicboiler.model_number,serial_number=hydronicboiler.serial_number,year_built=hydronicboiler.year_built,input_capacity=hydronicboiler.input_capacity,output_capacity=hydronicboiler.output_capacity,effciency=hydronicboiler.heating_eff,boiler_type=hydronicboiler.type_boiler,lhwt=hydronicboiler.lhwt,ehwt=hydronicboiler.ehwt,area=hydronicboiler.area)
            db.session.add(hydronic_boiler)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = hydronicboiler.area_id))
    else:
        abort(403)


@clientcommercial.route("/add_furnace/<int:id>", methods=['GET', 'POST'])
@login_required
def add_furnace(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = FurnaceForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            heating_eff = request.form['heating_eff']
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            furnace = Furnace(building_id = building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=heating_eff,area=area)
            try:
                db.session.add(furnace)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding furnace"
        else:
            return render_template('add_hvac_equipment.html', add='furnace',area=area, form=form)
    else:
        abort(403)
@clientcommercial.route("/add_furnace/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_furnace(id):
    if(current_user.is_authenticated and current_user.is_client()):
        furnace = Furnace.query.get_or_404(id)
        area = furnace.area_id
        form = FurnaceForm()
        if form.validate_on_submit():
           furnace.manufacturer = form.manufacturer.data
           furnace.model_number = form.model_number.data
           furnace.serial_number = form.serial_number.data 
           furnace.year_built = form.year_built.data
           furnace.input_capacity = form.input_capacity.data
           furnace.output_capacity = form.output_capacity.data 
           furnace.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = furnace.manufacturer   
            form.model_number.data = furnace.model_number
            form.serial_number.data = furnace.serial_number 
            form.year_built.data = furnace.year_built
            form.input_capacity.data = furnace.input_capacity   
            form.output_capacity.data = furnace.output_capacity
            form.heating_eff.data = furnace.effciency 
        return render_template('add_hvac_equipment.html', add='furnace',area=area,form=form)
    else:
        abort(403)




@clientcommercial.route('/add_furnace/<int:id>/delete', methods=['POST'])
@login_required
def deletefurnace(id):
    if(current_user.is_authenticated and current_user.is_client()):
        furnace = Furnace.query.get_or_404(id)
        area = furnace.area_id
        db.session.delete(furnace)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)


@clientcommercial.route('/duplicatefurnace/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatefurnace(id):
    if(current_user.is_authenticated and current_user.is_client()):
        furnace_id = id
        furnace = Furnace.query.get(id)
        form = FurnaceForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_furnace = Furnace(building_id = furnace.building,photo=furnace.photo, manufacturer=furnace.manufacturer,model_number=furnace.model_number,serial_number=furnace.serial_number,year_built=furnace.year_built,input_capacity=furnace.input_capacity,output_capacity=furnace.output_capacity,effciency=furnace.heating_eff,area=furnace.area)
            db.session.add(new_furnace)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = furnace.area_id))
    else:
        abort(403)


@clientcommercial.route("/add_unit_heater/<int:id>", methods=['GET', 'POST'])
@login_required
def add_unit_heater(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = UnitHeaterForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            supply_air_temp = request.form["supply_air_temp"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            heating_eff = request.form['heating_eff']
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            unit_heater = UnitHeater(building_id = building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=heating_eff,supply_air_temp=supply_air_temp,area=area)
            try:
                db.session.add(unit_heater)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding unit heater"
        else:
            return render_template('add_hvac_equipment.html', add='unit_heater',area=area, form=form)
    else:
        abort(403)
@clientcommercial.route("/add_unit_heater/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_unit_heater(id):
    if(current_user.is_authenticated and current_user.is_client()):
        unit_heater = UnitHeater.query.get_or_404(id)
        area = unit_heater.area_id
        form = UnitHeaterForm()
        if form.validate_on_submit():
           unit_heater.manufacturer = form.manufacturer.data
           unit_heater.model_number = form.model_number.data
           unit_heater.serial_number = form.serial_number.data 
           unit_heater.year_built = form.year_built.data
           unit_heater.input_capacity = form.input_capacity.data
           unit_heater.output_capacity = form.output_capacity.data 
           unit_heater.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = unit_heater.manufacturer   
            form.model_number.data = unit_heater.model_number
            form.serial_number.data = unit_heater.serial_number 
            form.year_built.data = unit_heater.year_built
            form.input_capacity.data = unit_heater.input_capacity   
            form.output_capacity.data = unit_heater.output_capacity
            form.heating_eff.data = unit_heater.effciency 
        return render_template('add_hvac_equipment.html', add='unit_heater',area=area,form=form)
    else:
        abort(403)


@clientcommercial.route('/add_unit_heater/<int:id>/delete', methods=['POST'])
@login_required
def deleteunitheater(id):
    if(current_user.is_authenticated and current_user.is_client()):
        unit_heatern = UnitHeater.query.get_or_404(id)
        area = unit_heatern.area_id
        db.session.delete(unit_heatern)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@clientcommercial.route('/duplicateunitheater/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateunitheater(id):
    if(current_user.is_authenticated and current_user.is_client()):
        unitheater_id = id
        unitheater = UnitHeater.query.get(id)
        form = UnitHeaterForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            unit_heater = UnitHeater(building_id = unitheater.building,photo=unitheater.photo, manufacturer=unitheater.manufacturer,model_number=unitheater.model_number,serial_number=unitheater.serial_number,year_built=unitheater.year_built,input_capacity=unitheater.input_capacity,output_capacity=unitheater.output_capacity,effciency=unitheater.heating_eff,supply_air_temp=unitheater.supply_air_temp,area=unitheater.area)
            db.session.add(unit_heater)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = unitheater.area_id))
    else:
        abort(403)

@clientcommercial.route("/add_gas_fired_heating_coil/<int:id>", methods=['GET', 'POST'])
@login_required
def add_gas_fired_heating_coil(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = GasFiredHeatingCoilForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            efficiency = request.form['heating_eff']
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            gas_fired_heating_coil = GasFiredHeatingCoil(building_id = building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=efficiency,area=area)
            try:
                db.session.add(gas_fired_heating_coil)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding gas fired heating coil"
        else:
            return render_template('add_hvac_equipment.html', add='gas_fired_heating_coil',area=area,form=form)
    else:
        abort(403)

@clientcommercial.route("/add_gas_fired_heating_coil/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_gas_fired_heating_coil(id):
    if(current_user.is_authenticated and current_user.is_client()):
        gas_fired_heating_coil = GasFiredHeatingCoil.query.get_or_404(id)
        area = gas_fired_heating_coil.area_id
        form = GasFiredHeatingCoilForm()
        if form.validate_on_submit():
           gas_fired_heating_coil.manufacturer = form.manufacturer.data
           gas_fired_heating_coil.model_number = form.model_number.data
           gas_fired_heating_coil.serial_number = form.serial_number.data 
           gas_fired_heating_coil.year_built = form.year_built.data
           gas_fired_heating_coil.input_capacity = form.input_capacity.data
           gas_fired_heating_coil.output_capacity = form.output_capacity.data 
           gas_fired_heating_coil.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = gas_fired_heating_coil.manufacturer   
            form.model_number.data = gas_fired_heating_coil.model_number
            form.serial_number.data = gas_fired_heating_coil.serial_number 
            form.year_built.data = gas_fired_heating_coil.year_built
            form.input_capacity.data = gas_fired_heating_coil.input_capacity   
            form.output_capacity.data = gas_fired_heating_coil.output_capacity
            form.heating_eff.data = gas_fired_heating_coil.effciency 
        return render_template('add_hvac_equipment.html', add='gas_fired_heating_coil',area=area,form=form)
    else:
        abort(403)

@clientcommercial.route('/add_gas_fired_heating_coil/<int:id>/delete', methods=['POST'])
@login_required
def deletegasfiredheatingcoil(id):
    if(current_user.is_authenticated and current_user.is_client()):
        gas_fired_heating_coil = GasFiredHeatingCoil.query.get_or_404(id)
        area = gas_fired_heating_coil.area_id
        db.session.delete(gas_fired_heating_coil)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@clientcommercial.route('/duplicategasfiredheatingcoil/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicategasfiredheatingcoil(id):
    if(current_user.is_authenticated and current_user.is_client()):
        gasfiredheatingcoil_id = id
        gasfiredheatingcoil = GasFiredHeatingCoil.query.get(id)
        form = GasFiredHeatingCoilForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            gas_fired_heating_coil = GasFiredHeatingCoil(building_id = gasfiredheatingcoil.building,photo=gasfiredheatingcoil.photo, manufacturer=gasfiredheatingcoil.manufacturer,model_number=gasfiredheatingcoil.model_number,serial_number=gasfiredheatingcoil.serial_number,year_built=gasfiredheatingcoil.year_built,input_capacity=gasfiredheatingcoil.input_capacity,output_capacity=gasfiredheatingcoil.output_capacity,effciency=gasfiredheatingcoil.efficiency,area=gasfiredheatingcoil.area)
            db.session.add(gas_fired_heating_coil)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = gasfiredheatingcoil.area_id))
    else:
        abort(403)

@clientcommercial.route("/add_heat_pump/<int:id>", methods=['GET', 'POST'])
@login_required
def add_heat_pump(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = HeatPumpForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            fuel_type = request.form['fuel_type']
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            heat_pump = HeatPump(building_id=building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,fuel_type=fuel_type,area=area)
            try:
                db.session.add(heat_pump)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding heat pump"

        else:
            return render_template('add_hvac_equipment.html', add='heat_pump',area=area,form=form)
    else:
        abort(403)
@clientcommercial.route("/add_heat_pump/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_heat_pump(id):
    if(current_user.is_authenticated and current_user.is_client()):
        heat_pump = HeatPump.query.get_or_404(id)
        area = heat_pump.area_id
        form = HeatPumpForm()
        if form.validate_on_submit():
           heat_pump.manufacturer = form.manufacturer.data
           heat_pump.model_number = form.model_number.data
           heat_pump.serial_number = form.serial_number.data 
           heat_pump.year_built = form.year_built.data
           heat_pump.fuel_type = form.fuel_type.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = heat_pump.manufacturer   
            form.model_number.data = heat_pump.model_number
            form.serial_number.data = heat_pump.serial_number 
            form.year_built.data = heat_pump.year_built
            form.fuel_type.data = heat_pump.fuel_type
        return render_template('add_hvac_equipment.html', add='heat_pump',area=area,form=form)
    else:
        abort(403)


@clientcommercial.route('/add_heat_pump/<int:id>/delete', methods=['POST'])
@login_required
def deleteheatpump(id):
    if(current_user.is_authenticated and current_user.is_client()):
        heat_pump = HeatPump.query.get_or_404(id)
        area = heat_pump.area_id
        db.session.delete(heat_pump)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@clientcommercial.route('/duplicateheatpump/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateheatpump(id):
    if(current_user.is_authenticated and current_user.is_client()):
        heatpump_id = id
        heatpump = HeatPumpForm.query.get(id)
        form = GasFiredHeatingCoilForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            heat_pump = HeatPump(building=heatpump.building_id,photo=heatpump.photo, manufacturer=heatpump.manufacturer,model_number=heatpump.model_number,serial_number=heatpump.serial_number,year_built=heatpump.year_built,fuel_type=heatpump.fuel_type,area=heatpump.area)
            db.session.add(heat_pump)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = heatpump.area_id))
    else:
        abort(403)

@clientcommercial.route("/add_electric_rest_heating_coil/<int:id>", methods=['GET', 'POST'])
@login_required
def addelectricrestheatingcoil(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = ElectricRestHeatingCoilForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            efficiency = request.form['heating_eff']
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            electric_rest_heating_coil = ElectricRestHeatingCoil(building_id=building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=efficiency,area=area)
            try:
                db.session.add(electric_rest_heating_coil)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding electric rest heating coil"
        else:
            return render_template('add_hvac_equipment.html', add='electric_rest_heating_coil',area=area, form=form)
    else:
        abort(403)

@clientcommercial.route("/add_electric_rest_heating_coil/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_electric_rest_heating_coil(id):
    if(current_user.is_authenticated and current_user.is_client()):
        electric_rest_heating_coil = ElectricRestHeatingCoil.query.get_or_404(id)
        area = electric_rest_heating_coil.area_id
        form = ElectricRestHeatingCoilForm()
        if form.validate_on_submit():
           electric_rest_heating_coil.manufacturer = form.manufacturer.data
           electric_rest_heating_coil.model_number = form.model_number.data
           electric_rest_heating_coil.serial_number = form.serial_number.data 
           electric_rest_heating_coil.year_built = form.year_built.data
           electric_rest_heating_coil.input_capacity = form.input_capacity.data
           electric_rest_heating_coil.output_capacity = form.output_capacity.data 
           electric_rest_heating_coil.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = electric_rest_heating_coil.manufacturer   
            form.model_number.data = electric_rest_heating_coil.model_number
            form.serial_number.data = electric_rest_heating_coil.serial_number 
            form.year_built.data = electric_rest_heating_coil.year_built
            form.input_capacity.data = electric_rest_heating_coil.input_capacity   
            form.output_capacity.data = electric_rest_heating_coil.output_capacity
            form.heating_eff.data = electric_rest_heating_coil.effciency 
        return render_template('add_hvac_equipment.html', add='electric_rest_heating_coil',area=area,form=form)
    else:
        abort(403)


@clientcommercial.route('/add_electric_rest_heating_coil/<int:id>/delete', methods=['POST'])
@login_required
def deleteelectricrestheatingcoil(id):
    if(current_user.is_authenticated and current_user.is_client()):
        electric_rest_heating_coil = ElectricRestHeatingCoil.query.get_or_404(id)
        area = electric_rest_heating_coil.area_id
        db.session.delete(electric_rest_heating_coil)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@clientcommercial.route('/duplicateelectricrestheatingcoil/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateelectricrestheatingcoil(id):
    if(current_user.is_authenticated and current_user.is_client()):
        electricrestheatingcoil_id = id
        electricrestheatingcoil = ElectricRestHeatingCoil.query.get(id)
        form = ElectricRestHeatingCoilForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            electric_rest_heating_coil = ElectricRestHeatingCoil(building=electricrestheatingcoil.building_id,photo=electricrestheatingcoil.photo, manufacturer=electricrestheatingcoil.manufacturer,model_number=electricrestheatingcoil.model_number,serial_number=electricrestheatingcoil.serial_number,year_built=electricrestheatingcoil.year_built,input_capacity=electricrestheatingcoil.input_capacity,output_capacity=electricrestheatingcoil.output_capacity,effciency=electricrestheatingcoil.efficiency,area=electricrestheatingcoil.area)
            db.session.add(electric_rest_heating_coil)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = electricrestheatingcoil.area_id))
    else:
        abort(403)



@clientcommercial.route("/add_infrared_heater/<int:id>", methods=['GET', 'POST'])
@login_required
def add_infrared_heater(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = InfraredHeaterForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            heating_eff = request.form['heating_eff']
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            infrared_heater = InfraredHeater(building_id = building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=heating_eff,area=area)
            try:
                db.session.add(infrared_heater)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding infrared_heater"
        else:
            return render_template('add_hvac_equipment.html', add='infrared_heater',area=area, form=form)
    else:
        abort(403)
@clientcommercial.route("/add_infrared_heater/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_infrared_heater(id):
    if(current_user.is_authenticated and current_user.is_client()):
        infrared_heater = InfraredHeater.query.get_or_404(id)
        area = infrared_heater.area_id
        form = InfraredHeaterForm()
        if form.validate_on_submit():
           infrared_heater.manufacturer = form.manufacturer.data
           infrared_heater.model_number = form.model_number.data
           infrared_heater.serial_number = form.serial_number.data 
           infrared_heater.year_built = form.year_built.data
           infrared_heater.input_capacity = form.input_capacity.data
           infrared_heater.output_capacity = form.output_capacity.data 
           infrared_heater.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = infrared_heater.manufacturer   
            form.model_number.data = infrared_heater.model_number
            form.serial_number.data = infrared_heater.serial_number 
            form.year_built.data = infrared_heater.year_built
            form.input_capacity.data = infrared_heater.input_capacity   
            form.output_capacity.data = infrared_heater.output_capacity
            form.heating_eff.data = infrared_heater.effciency 
        return render_template('add_hvac_equipment.html', add='infrared_heater',area=area,form=form)
    else:
        abort(403)


@clientcommercial.route('/add_infrared_heater/<int:id>/delete', methods=['POST'])
@login_required
def deleteinfraredheater(id):
    if(current_user.is_authenticated and current_user.is_client()):
        infrared_heater = InfraredHeater.query.get_or_404(id)
        area = infrared_heater.area_id
        db.session.delete(infrared_heater)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)


@clientcommercial.route('/duplicateinfraredheater/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateinfraredheater(id):
    if(current_user.is_authenticated and current_user.is_client()):
        infraredheater_id = id
        infraredheater = InfraredHeater.query.get(id)
        form = InfraredHeaterForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            infrared_heater = InfraredHeater(building_id = infraredheater.building_id,photo=infraredheater.photo, manufacturer=infraredheater.manufacturer,model_number=infraredheater.model_number,serial_number=infraredheater.serial_number,year_built=infraredheater.year_built,input_capacity=infraredheater.input_capacity,output_capacity=infraredheater.output_capacity,effciency=infraredheater.heating_eff,area=infraredheater.area)
            db.session.add(infrared_heater)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = infraredheater.area_id))
    else:
        abort(403)
@clientcommercial.route("/add_make_up_air_unit/<int:id>", methods=['GET', 'POST'])
@login_required
def add_make_up_air_unit(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = MakeUpAirUnitForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            cooling_capacity = request.form["cooling_capacity"]
            cooling_coil_type = request.form["cooling_coil_type"]
            compressor_type = request.form["compressor_type"]
            heating_capacity = request.form["heating_capacity"]
            heating_coil_type = request.form["heating_coil_type"]
            heating_eff = request.form['heating_eff']
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            make_up_air_unit = MakeUpAirUnit(building_id=building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,cooling_capacity=cooling_capacity,cooling_coil_type=cooling_coil_type,heating_capacity=heating_capacity,heating_coil_type=heating_coil_type,effciency=heating_eff,area=area)
            try:
                db.session.add(make_up_air_unit)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding make up air unit"
        else:
            return render_template('add_hvac_equipment.html', add='make_up_air_unit',area=area, form=form)
    else:
        abort(403)

@clientcommercial.route("/add_make_up_air_unit/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_make_up_air_unit(id):
    if(current_user.is_authenticated and current_user.is_client()):
        make_up_air_unit = MakeUpAirUnit.query.get_or_404(id)
        area = make_up_air_unit.area_id
        form = MakeUpAirUnitForm()
        if form.validate_on_submit():
           make_up_air_unit.manufacturer = form.manufacturer.data
           make_up_air_unit.model_number = form.model_number.data
           make_up_air_unit.serial_number = form.serial_number.data 
           make_up_air_unit.year_built = form.year_built.data
           make_up_air_unit.cooling_capacity = form.cooling_capacity.data
           make_up_air_unit.cooling_coil_type = form.cooling_coil_type.data
           make_up_air_unit.heating_capacity = form.heating_capacity.data
           make_up_air_unit.heating_coil_type = form.heating_coil_type.data
           make_up_air_unit.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = make_up_air_unit.manufacturer   
            form.model_number.data = make_up_air_unit.model_number
            form.serial_number.data = make_up_air_unit.serial_number 
            form.year_built.data = make_up_air_unit.year_built
            form.cooling_capacity.data = make_up_air_unit.cooling_capacity
            form.cooling_coil_type.data = make_up_air_unit.cooling_coil_type 
            form.heating_capacity.data = make_up_air_unit.heating_capacity
            form.heating_coil_type.data = make_up_air_unit.heating_coil_type
            form.heating_eff.data = make_up_air_unit.effciency 
        return render_template('add_hvac_equipment.html', add='make_up_air_unit',area=area,form=form)
    else:
        abort(403)


@clientcommercial.route('/add_make_up_air_unit/<int:id>/delete', methods=['POST'])
@login_required
def deletemakeupairunit(id):
    if(current_user.is_authenticated and current_user.is_client()):
        make_up_air_unit = MakeUpAirUnit.query.get_or_404(id)
        area = make_up_air_unit.area_id
        db.session.delete(make_up_air_unit)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@clientcommercial.route('/duplicatemakeupairunit/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatemakeupairunit(id):
    if(current_user.is_authenticated and current_user.is_client()):
        makeupairunit_id = id
        makeupairunit = MakeUpAirUnit.query.get(id)
        form = MakeUpAirUnitForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            make_up_air_unit = InfraredHeater(building_id = makeupairunit.building_id,photo=makeupairunit.photo, manufacturer=makeupairunit.manufacturer,model_number=makeupairunit.model_number,serial_number=makeupairunit.serial_number,year_built=makeupairunit.year_built,input_capacity=makeupairunit.input_capacity,output_capacity=makeupairunit.output_capacity,effciency=makeupairunit.heating_eff,area=makeupairunit.area)
            db.session.add(make_up_air_unit)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = makeupairunit.area_id))
    else:
        abort(403)

@clientcommercial.route("/add_packaged_rtu/<int:id>", methods=['GET', 'POST'])
@login_required
def add_packaged_rtu(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = PackagedRTUForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            compressor_type = request.form['compressor_type']
            cooling_capacity = request.form["cooling_capacity"]
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            heating_capacity = request.form["heating_capacity"]
            heating_coil_type = request.form["heating_coil_type"]
            heating_eff = request.form['heating_eff']
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            packaged_rtu = PackagedRTU(building_id=building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,cooling_capacity=cooling_capacity,compressor_type=compressor_type,refridgerant=refridgerant,kwton=kwton,eer=eer,heating_capacity=heating_capacity,heating_coil_type=heating_coil_type,effciency=heating_eff,area=area)
            try:
                db.session.add(packaged_rtu)
                db.session.commit()
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding make up air unit"
        else:
            return render_template('add_hvac_equipment.html', add='packaged_rtu',area=area, form=form)
    else:
        abort(403)
@clientcommercial.route("/add_packaged_rtu/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_packaged_rtu(id):
    if(current_user.is_authenticated and current_user.is_client()):
        packaged_rtu = PackagedRTU.query.get_or_404(id)
        area = packaged_rtu.area_id
        form = PackagedRTUForm()
        if form.validate_on_submit():
           packaged_rtu.manufacturer = form.manufacturer.data
           packaged_rtu.model_number = form.model_number.data
           packaged_rtu.serial_number = form.serial_number.data 
           packaged_rtu.year_built = form.year_built.data
           packaged_rtu.compressor_type = form.compressor_type.data
           packaged_rtu.cooling_capacity = form.cooling_capacity.data
           packaged_rtu.refridgerant = form.refridgerant.data
           packaged_rtu.kwton = form.kwton.data
           packaged_rtu.eer = form.eer.data
           packaged_rtu.heating_capacity = form.heating_capacity.data
           packaged_rtu.heating_coil_type = form.heating_coil_type.data
           packaged_rtu.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = packaged_rtu.manufacturer   
            form.model_number.data = packaged_rtu.model_number
            form.serial_number.data = packaged_rtu.serial_number 
            form.year_built.data = packaged_rtu.year_built
            form.cooling_capacity.data = packaged_rtu.cooling_capacity
            form.compressor_type.data = packaged_rtu.compressor_type 
            form.refridgerant.data = packaged_rtu.refridgerant
            form.kwton.data = packaged_rtu.kwton
            form.eer.data = packaged_rtu.eer
            form.heating_capacity.data = packaged_rtu.heating_capacity
            form.heating_coil_type.data = packaged_rtu.heating_coil_type
            form.heating_eff.data = packaged_rtu.effciency 
        return render_template('add_hvac_equipment.html', add='packaged_rtu',area=area,form=form)
    else:
        abort(403)

@clientcommercial.route('/add_packaged_rtu/<int:id>/delete', methods=['POST'])
@login_required
def deletepackagedrtu(id):
    if(current_user.is_authenticated and current_user.is_client()):
        packaged_rtu = PackagedRTU.query.get_or_404(id)
        area = packaged_rtu.area_id
        db.session.delete(packaged_rtu)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)

@clientcommercial.route('/duplicatepackagedrtu/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatepackagedrtu(id):
    if(current_user.is_authenticated and current_user.is_client()):
        packagedrtu_id = id
        packagedrtu = PackagedRTU.query.get(id)
        form = PackagedRTUForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            packaged_rtu = PackagedRTU(building_id = packagedrtu.building_id,photo=packagedrtu.photo, manufacturer=packagedrtu.manufacturer,model_number=packagedrtu.model_number,serial_number=packagedrtu.serial_number,year_built=packagedrtu.year_built,input_capacity=packagedrtu.input_capacity,output_capacity=packagedrtu.output_capacity,effciency=packagedrtu.heating_eff,area=packagedrtu.area)
            db.session.add(packaged_rtu)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = packagedrtu.area_id))
    else:
        abort(403)

@clientcommercial.route("/add_chiller/<int:id>", methods=['GET', 'POST'])
@login_required
def add_chiller(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = ChillerForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            cooling_capacity = request.form["cooling_capacity"]
            compressor_type = request.form['compressor_type']
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            type_chiller = request.form["chiller_type"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            chiller = Chiller(building_id=building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,cooling_capacity=cooling_capacity, compressor_type=compressor_type,refridgerant=refridgerant,kwton=kwton,eer=eer,type_chiller=type_chiller,area=area)
            try:
                db.session.add(chiller)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding make up air unit"
        else:
            return render_template('add_hvac_equipment.html', add='chiller',area=area, form=form)
    else:
        abort(403)
@clientcommercial.route("/add_chiller/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_chiller(id):
    if(current_user.is_authenticated and current_user.is_client()):
        chiller = Chiller.query.get_or_404(id)
        area = chiller.area_id
        form = ChillerForm()
        if form.validate_on_submit():
           chiller.manufacturer = form.manufacturer.data
           chiller.model_number = form.model_number.data
           chiller.serial_number = form.serial_number.data 
           chiller.year_built = form.year_built.data
           chiller.compressor_type = form.compressor_type.data
           chiller.cooling_capacity = form.cooling_capacity.data
           chiller.refridgerant = form.refridgerant.data
           chiller.kwton = form.kwton.data
           chiller.eer = form.eer.data
           chiller.type_chiller = form.chiller_type.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = chiller.manufacturer   
            form.model_number.data = chiller.model_number
            form.serial_number.data = chiller.serial_number 
            form.year_built.data = chiller.year_built
            form.cooling_capacity.data = chiller.cooling_capacity
            form.compressor_type.data = chiller.compressor_type 
            form.refridgerant.data = chiller.refridgerant
            form.kwton.data = chiller.kwton
            form.eer.data = chiller.eer
            form.chiller_type.data = chiller.type_chiller
        return render_template('add_hvac_equipment.html', add='chiller',area=area,form=form)
    else:
        abort(403)

@clientcommercial.route('/add_chiller/<int:id>/delete', methods=['POST'])
@login_required
def deletechiller(id):
    if(current_user.is_authenticated and current_user.is_client()):
        chiller = Chiller.query.get_or_404(id)
        area = chiller.area_id
        db.session.delete(chiller)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@clientcommercial.route('/duplicatechiller/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatechiller(id):
    if(current_user.is_authenticated and current_user.is_client()):
        chiller_id = id
        chiller = Chiller.query.get(id)
        form = ChillerForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_chiller = PackagedRTU(building_id = chiller.building_id,photo=chiller.photo, manufacturer=chiller.manufacturer,model_number=chiller.model_number,serial_number=chiller.serial_number,year_built=chiller.year_built,input_capacity=chiller.input_capacity,output_capacity=chiller.output_capacity,effciency=chiller.heating_eff,area=chiller.area)
            db.session.add(new_chiller)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = chiller.area_id))
    else:
        abort(403)
@clientcommercial.route("/add_mini_split_system/<int:id>", methods=['GET', 'POST'])
@login_required
def add_mini_split_system(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = MiniSplitSystemForm()


        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            compressor_type = request.form['compressor_type']
            cooling_capacity = request.form["cooling_capacity"]
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            mini_split_system = MiniSplitSystem(building_id=building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,
                        year_built=year_built,compressor_type=compressor_type,cooling_capacity=cooling_capacity,refridgerant=refridgerant,
                        kwton=kwton,eer=eer,area=area)
            try:
                db.session.add(mini_split_system)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+ str(id))
            except:
                return "There was an error adding mini split system"
        else:
            return render_template('add_hvac_equipment.html', add='mini_split_system',area=area, form=form)
    else:
        abort(403)
@clientcommercial.route("/add_mini_split_system/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_mini_split_system(id):
    if(current_user.is_authenticated and current_user.is_client()):
        mini_split_system = MiniSplitSystem.query.get_or_404(id)
        area = mini_split_system.area_id
        form = MiniSplitSystemForm()
        if form.validate_on_submit():
           mini_split_system.manufacturer = form.manufacturer.data
           mini_split_system.model_number = form.model_number.data
           mini_split_system.serial_number = form.serial_number.data 
           mini_split_system.year_built = form.year_built.data
           mini_split_system.compressor_type = form.compressor_type.data
           mini_split_system.cooling_capacity = form.cooling_capacity.data
           mini_split_system.refridgerant = form.refridgerant.data
           mini_split_system.kwton = form.kwton.data
           mini_split_system.eer = form.eer.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = mini_split_system.manufacturer   
            form.model_number.data = mini_split_system.model_number
            form.serial_number.data = mini_split_system.serial_number 
            form.year_built.data = mini_split_system.year_built
            form.cooling_capacity.data = mini_split_system.cooling_capacity
            form.compressor_type.data = mini_split_system.compressor_type 
            form.refridgerant.data = mini_split_system.refridgerant
            form.kwton.data = mini_split_system.kwton
            form.eer.data = mini_split_system.eer
        return render_template('add_hvac_equipment.html', add='mini_split_system',area=area,form=form)
    else:
        abort(403)


@clientcommercial.route('/add_mini_split_system/<int:id>/delete', methods=['POST'])
@login_required
def deleteminisplitsystem(id):
    if(current_user.is_authenticated and current_user.is_client()):
        mini_split_system = MiniSplitSystem.query.get_or_404(id)
        area = mini_split_system.area_id
        db.session.delete(mini_split_system)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@clientcommercial.route('/duplicateminisplitsystem/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateminisplitsystem(id):
    if(current_user.is_authenticated and current_user.is_client()):
        minisplitsystem_id = id
        minisplitsystem = MiniSplitSystem.query.get(id)
        form = MiniSplitSystemForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            mini_split_system = MiniSplitSystem(building_id = minisplitsystem.building_id,photo=minisplitsystem.photo, manufacturer=minisplitsystem.manufacturer,model_number=minisplitsystem.model_number,serial_number=minisplitsystem.serial_number,year_built=minisplitsystem.year_built,input_capacity=minisplitsystem.input_capacity,output_capacity=minisplitsystem.output_capacity,effciency=minisplitsystem.heating_eff,area=minisplitsystem.area)
            db.session.add(mini_split_system)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = minisplitsystem.area_id))
    else:
        abort(403)
@clientcommercial.route("/add_packaged_terminal_ac/<int:id>", methods=['GET', 'POST'])
@login_required
def add_packaged_terminal_ac(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = PackagedTerminalACForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            compressor_type = request.form['compressor_type']
            cooling_capacity = request.form["cooling_capacity"]
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            packaged_terminal_ac = PackagedTerminalAC(building=building_id,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,
                        year_built=year_built,compressor_type=compressor_type,cooling_capacity=cooling_capacity,refridgerant=refridgerant,
                        kwton=kwton,eer=eer,area=area)
            try:
                db.session.add(packaged_terminal_ac)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding packaged terminal AC"

        else:
            return render_template('add_hvac_equipment.html', add='packaged_terminal_ac',area=area, form=form)
    else:
        abort(403)
@clientcommercial.route("/add_packaged_terminal_ac/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_packaged_terminal_ac(id):
    if(current_user.is_authenticated and current_user.is_client()):
        packaged_terminal_ac = PackagedTerminalAC.query.get_or_404(id)
        area = packaged_terminal_ac.area_id
        form = PackagedTerminalACForm()
        if form.validate_on_submit():
           packaged_terminal_ac.manufacturer = form.manufacturer.data
           packaged_terminal_ac.model_number = form.model_number.data
           packaged_terminal_ac.serial_number = form.serial_number.data 
           packaged_terminal_ac.year_built = form.year_built.data
           packaged_terminal_ac.compressor_type = form.compressor_type.data
           packaged_terminal_ac.cooling_capacity = form.cooling_capacity.data
           packaged_terminal_ac.refridgerant = form.refridgerant.data
           packaged_terminal_ac.kwton = form.kwton.data
           packaged_terminal_ac.eer = form.eer.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = packaged_terminal_ac.manufacturer   
            form.model_number.data = packaged_terminal_ac.model_number
            form.serial_number.data = packaged_terminal_ac.serial_number 
            form.year_built.data = packaged_terminal_ac.year_built
            form.cooling_capacity.data = packaged_terminal_ac.cooling_capacity
            form.compressor_type.data = packaged_terminal_ac.compressor_type 
            form.refridgerant.data = packaged_terminal_ac.refridgerant
            form.kwton.data = packaged_terminal_ac.kwton
            form.eer.data = packaged_terminal_ac.eer
        return render_template('add_hvac_equipment.html', add='packaged_terminal_ac',area=area,form=form)
    else:
        abort(403)

@clientcommercial.route('/add_packaged_terminal_ac/<int:id>/delete', methods=['POST'])
@login_required
def deletepackagedterminalac(id):
    if(current_user.is_authenticated and current_user.is_client()):
        packaged_terminal_ac = PackagedTerminalAC.query.get_or_404(id)
        area = packaged_terminal_ac.area_id
        db.session.delete(packaged_terminal_ac)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@clientcommercial.route('/duplicatepackagedterminalac/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatepackagedterminalac(id):
    if(current_user.is_authenticated and current_user.is_client()):
        packagedterminalac_id = id
        packagedterminalac = PackagedTerminalAC.query.get(id)
        form = PackagedTerminalACForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            packaged_terminal_ac = PackagedTerminalAC(building_id = packagedterminalac.building_id,photo=packagedterminalac.photo, manufacturer=packagedterminalac.manufacturer,model_number=packagedterminalac.model_number,serial_number=packagedterminalac.serial_number,year_built=packagedterminalac.year_built,input_capacity=packagedterminalac.input_capacity,output_capacity=packagedterminalac.output_capacity,effciency=packagedterminalac.heating_eff,area=packagedterminalac.area)
            db.session.add(packaged_terminal_ac)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = packagedterminalac.area_id))
    else:
        abort(403)

@clientcommercial.route("/add_condensing_unit_system/<int:id>", methods=['GET', 'POST'])
@login_required
def add_condensing_unit_system(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = CondensingUnitSystemForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            compressor_type = request.form["compressor_type"]
            cooling_capacity = request.form["cooling_capacity"]
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            condensing_unit_system= CondensingUnitSystem(building=building_id,photo=photo, manufacturer=manufacturer,model_number=model_number,
                        serial_number=serial_number,year_built=year_built,compressor_type=compressor_type,cooling_capacity=cooling_capacity,refridgerant=refridgerant,
                        kwton=kwton,eer=eer,area=area)
            try:
                db.session.add(condensing_unit_system)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error condesnsingu unit system"
        else:
            return render_template('add_hvac_equipment.html', add='condensing_unit_system',area=area, form=form)
    else:
        abort(403)
@clientcommercial.route("/add_condensing_unit_system/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_condensing_unit_system(id):
    if(current_user.is_authenticated and current_user.is_client()):
        condensing_unit_system = CondensingUnitSystem.query.get_or_404(id)
        area = condensing_unit_system.area_id
        form = CondensingUnitSystemForm()
        if form.validate_on_submit():
           condensing_unit_system.manufacturer = form.manufacturer.data
           condensing_unit_system.model_number = form.model_number.data
           condensing_unit_system.serial_number = form.serial_number.data 
           condensing_unit_system.year_built = form.year_built.data
           condensing_unit_system.compressor_type = form.compressor_type.data
           condensing_unit_system.cooling_capacity = form.cooling_capacity.data
           condensing_unit_system.refridgerant = form.refridgerant.data
           condensing_unit_system.kwton = form.kwton.data
           condensing_unit_system.eer = form.eer.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = condensing_unit_system.manufacturer   
            form.model_number.data = condensing_unit_system.model_number
            form.serial_number.data = condensing_unit_system.serial_number 
            form.year_built.data = condensing_unit_system.year_built
            form.cooling_capacity.data = condensing_unit_system.cooling_capacity
            form.compressor_type.data = condensing_unit_system.compressor_type 
            form.refridgerant.data = condensing_unit_system.refridgerant
            form.kwton.data = condensing_unit_system.kwton
            form.eer.data = condensing_unit_system.eer
        return render_template('add_hvac_equipment.html', add='condensing_unit_system',area=area,form=form)
    else:
        abort(403)


@clientcommercial.route('/add_condensing_unit_system/<int:id>/delete', methods=['POST'])
@login_required
def deletecondensingunitsystem(id):
    if(current_user.is_authenticated and current_user.is_client()):
        condensing_unit_system = CondensingUnitSystem.query.get_or_404(id)
        area = condensing_unit_system.area_id
        db.session.delete(condensing_unit_system)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)

@clientcommercial.route('/duplicatecondensingunitsystem/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatecondensingunitsystem(id):
    if(current_user.is_authenticated and current_user.is_client()):
        condensingunitsystem_id = id
        condensingunitsystem = CondensingUnitSystem.query.get(id)
        form = CondensingUnitSystemForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            condensing_unit_system = CondensingUnitSystem(building_id = condensingunitsystem.building_id,photo=condensingunitsystem.photo, manufacturer=condensingunitsystem.manufacturer,model_number=condensingunitsystem.model_number,serial_number=condensingunitsystem.serial_number,year_built=condensingunitsystem.year_built,input_capacity=condensingunitsystem.input_capacity,output_capacity=condensingunitsystem.output_capacity,effciency=condensingunitsystem.heating_eff,area=condensingunitsystem.area)
            db.session.add(condensing_unit_system)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = condensingunitsystem.area_id))
    else:
        abort(403)


@clientcommercial.route("/add_window_air_conditioner/<int:id>", methods=['GET', 'POST'])
@login_required
def add_window_air_conditioner(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = WindowAirConditionerForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            compressor_type = request.form['compressor_type']
            cooling_capacity = request.form["cooling_capacity"]
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            window_air_conditioner = WindowAirConditioner(building=building_id,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,compressor_type=compressor_type,cooling_capacity=cooling_capacity,refridgerant=refridgerant,kwton=kwton,eer=eer,area=area)
            try:
                db.session.add(window_air_conditioner)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding window air conditioner"
        else:
            return render_template('add_hvac_equipment.html', add='window_air_conditioner',area=area, form=form)
    else:
        abort(403)

@clientcommercial.route("/add_window_air_conditioner/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_window_air_conditioner(id):
    if(current_user.is_authenticated and current_user.is_client()):
        window_air_conditioner = WindowAirConditioner.query.get_or_404(id)
        area = window_air_conditioner.area_id
        form = WindowAirConditionerForm()
        if form.validate_on_submit():
           window_air_conditioner.manufacturer = form.manufacturer.data
           window_air_conditioner.model_number = form.model_number.data
           window_air_conditioner.serial_number = form.serial_number.data 
           window_air_conditioner.year_built = form.year_built.data
           window_air_conditioner.compressor_type = form.compressor_type.data
           window_air_conditioner.cooling_capacity = form.cooling_capacity.data
           window_air_conditioner.refridgerant = form.refridgerant.data
           window_air_conditioner.kwton = form.kwton.data
           window_air_conditioner.eer = form.eer.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = window_air_conditioner.manufacturer   
            form.model_number.data = window_air_conditioner.model_number
            form.serial_number.data = window_air_conditioner.serial_number 
            form.year_built.data = window_air_conditioner.year_built
            form.cooling_capacity.data = window_air_conditioner.cooling_capacity
            form.compressor_type.data = window_air_conditioner.compressor_type 
            form.refridgerant.data = window_air_conditioner.refridgerant
            form.kwton.data = window_air_conditioner.kwton
            form.eer.data = window_air_conditioner.eer
        return render_template('add_hvac_equipment.html', add='window_air_conditioner',area=area,form=form)
    else:
        abort(403)

@clientcommercial.route('/add_window_air_conditioner/<int:id>/delete', methods=['POST'])
@login_required
def deletewindowairconditioner(id):
    if(current_user.is_authenticated and current_user.is_client()):
        window_air_conditioner = WindowAirConditioner.query.get_or_404(id)
        area = window_air_conditioner.area_id
        db.session.delete(window_air_conditioner)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)


@clientcommercial.route('/duplicatewindowairconditioner/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatewindowairconditioner(id):
    if(current_user.is_authenticated and current_user.is_client()):
        windowairconditioner_id = id
        windowairconditioner = WindowAirConditioner.query.get(id)
        form = WindowAirConditionerForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            window_air_conditioner = WindowAirConditioner(building_id = windowairconditioner.building_id,photo=windowairconditioner.photo, manufacturer=windowairconditioner.manufacturer,model_number=windowairconditioner.model_number,serial_number=windowairconditioner.serial_number,year_built=windowairconditioner.year_built,input_capacity=windowairconditioner.input_capacity,output_capacity=windowairconditioner.output_capacity,effciency=windowairconditioner.heating_eff,area=windowairconditioner.area)
            db.session.add(window_air_conditioner)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = windowairconditioner.area_id))
    else:
        abort(403)



@clientcommercial.route("/add_motor/<int:id>", methods=['GET', 'POST'])
@login_required
def add_motor(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = MotorForm()
        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            condition = request.form["condition"]
            horsepower = request.form["horsepower"]
            rpm = request.form["rpm"]
            effciency = request.form["effciency"]
            volts = request.form['volts']
            bhp = request.form["bhp"]
            frame = request.form["frame"]
            fla = request.form["fla"]
            cfm = request.form["cfm"]
            phase = request.form["phase"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            motor =  Motor(photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,
                            condition=condition,horsepower=horsepower,rpm=rpm,effciency=effciency,volts=volts,bhp=bhp,
                            frame=frame,fla=fla,cfm=cfm,phase=phase,area=area,building_id = building)
            try:
                db.session.add(motor)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error motor"

        else:
            return render_template('add_hvac_equipment.html', add='motor',area=area, form=form)
    else:
        abort(403)


@clientcommercial.route('/duplicatemotor/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatemotor(id):
    if(current_user.is_authenticated and current_user.is_client()):
        motor_id = id
        motor = Motor.query.get(id)
        form = MotorForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_motor = Motor(building_id = motor.building_id,photo=motor.photo, manufacturer=motor.manufacturer,model_number=motor.model_number,serial_number=motor.serial_number,year_built=motor.year_built,input_capacity=motor.input_capacity,output_capacity=motor.output_capacity,effciency=motor.heating_eff,area=motor.area)
            db.session.add(new_motor)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = motor.area_id))
    else:
        abort(403)


@clientcommercial.route("/add_motor/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_motor(id):
    if(current_user.is_authenticated and current_user.is_client()):
        motor = Motor.query.get_or_404(id)
        area = motor.area_id
        form = MotorForm()
        if form.validate_on_submit():
           motor.manufacturer = form.manufacturer.data
           motor.model_number = form.model_number.data
           motor.serial_number = form.serial_number.data 
           motor.year_built = form.year_built.data
           motor.condition = form.condition.data
           motor.horsepower = form.horsepower.data
           motor.rpm = form.rpm.data
           motor.effciency = form.effciency.data
           motor.volts = form.volts.data
           motor.bhp = form.bhp.data
           motor.frame = form.frame.data
           motor.fla = form.fla.data
           motor.cfm = form.cfm.data
           motor.phase = form.phase.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = motor.manufacturer   
            form.model_number.data = motor.model_number
            form.serial_number.data = motor.serial_number 
            form.year_built.data = motor.year_built
            form.condition.data =  motor.condition
            form.horsepower.data = motor.horsepower
            form.rpm.data = motor.rpm
            form.effciency.data = motor.effciency
            form.volts.data = motor.volts
            form.bhp.data = motor.bhp
            form.frame.data = motor.frame
            form.fla.data = motor.fla
            form.cfm.data = motor.cfm
            form.phase.data = motor.phase
        return render_template('add_hvac_equipment.html', add='motor',area=area,form=form)
    else:
        abort(403)


@clientcommercial.route('/add_motor/<int:id>/delete', methods=['POST'])
@login_required
def deletemotor(id):
    if(current_user.is_authenticated and current_user.is_client()):
        motor = Motor.query.get_or_404(id)
        area = motor.area_id
        db.session.delete(motor)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)



@clientcommercial.route("/add_pump/<int:id>", methods=['GET', 'POST'])
@login_required
def add_pump(id):
    if(current_user.is_authenticated and current_user.is_client()):
        area = Area.query.get(id)
        building = area.building_id
        form = PumpForm()

        if request.method == 'POST':
            condition = request.form['condition']
            head = request.form["head"]
            gpm = request.form["gpm"]
            if form.validate_on_submit():
                for filename in request.files.getlist('photo'):
                    photo = Photo()
                    db.session.add(photo)
                    db.session.commit()
                    str_name='admin' + str(int(time.time()))
                    name = photo.id
                    photos.save(filename, name=str(name) + '.')
            pump =  Pump(photo=photo, condition=condition,head=head,gpm=gpm,area=area,building_id = building)
            try:
                db.session.add(pump)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding pump"

        else:
            return render_template('add_hvac_equipment.html', add='pump',area=area, form=form)
    else:
        abort(403)
@clientcommercial.route("/add_pump/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_pump(id):
    if(current_user.is_authenticated and current_user.is_client()):
        pump = Pump.query.get_or_404(id)
        area = pump.area_id
        form = PumpForm()
        if form.validate_on_submit():
           pump.condition = form.condition.data
           pump.head = form.head.data
           pump.gpm = form.gpm.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.condition.data =  pump.condition
            form.head.data = pump.head
            form.gpm.data = pump.gpm
        return render_template('add_hvac_equipment.html', add='pump',area=area,form=form)
    else:
        abort(403)



@clientcommercial.route('/add_pump/<int:id>/delete', methods=['POST'])
@login_required
def deletepump(id):
    if(current_user.is_authenticated and current_user.is_client()):
        pump = Pump.query.get_or_404(id)
        area = pump.area_id
        db.session.delete(pump)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)

@clientcommercial.route('/duplicatepump/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatepump(id):
    if(current_user.is_authenticated and current_user.is_client()):
        pump_id = id
        pump = Motor.query.get(id)
        form = MotorForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_pump = Motor(building_id = pump.building_id,photo=pump.photo, manufacturer=pump.manufacturer,model_number=pump.model_number,serial_number=pump.serial_number,year_built=pump.year_built,input_capacity=pump.input_capacity,output_capacity=pump.output_capacity,effciency=pump.heating_eff,area=pump.area)
            db.session.add(new_pump)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = pump.area_id))
    else:
        abort(403)

# photo uploading



# class Photo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     steam_boiler_photos = db.relationship('Steam_Boiler', backref='photo')
#     hydronic_boiler_photos = db.relationship('Hydronic_Boiler', backref='photo')

#     pump_photos = db.relationship('Pump', backref='photo')
#     motor_photos = db.relationship('Motor', backref='photo')

#     chiller_photos = db.relationship('Chiller', backref='photo')
#     furnace_photos = db.relationship('Furnace', backref='photo')
#     heatpump_photos = db.relationship('HeatPump', backref='photo')
#     pipe_photos = db.relationship('Pipe', backref='photo')
#     ahu_photos = db.relationship('AHU', backref='photo')
#     gasfiredheatingcoil_photos = db.relationship('GasFiredHeatingCoil', backref='photo')
#     electricrestheatingcoil_photos = db.relationship('ElectricRestHeatingCoil', backref='photo')
#     windowairconditioner_photos = db.relationship('WindowAirConditioner', backref='photo')
#     infraredheater_photo = db.relationship('InfraredHeater', backref='photo')
#     makeupairunit_photos = db.relationship('MakeUpAirUnit', backref='photo')
#     minisplitsystem_photos = db.relationship('MiniSplitSystem', backref='photo')
#     condensingunitsystem_photos = db.relationship('CondensingUnitSystem', backref='photo')
#     pakagedrtu_photos = db.relationship('PackagedRTU', backref='photo')
#     packagedterminalac_photos = db.relationship('PackagedTerminalAC', backref='photo')
#     selfcontainedahu_photos = db.relationship('SelfContainedAHU', backref='photo')
#     unitheater_photos = db.relationship('UnitHeater', backref='photo')
#     unitventilator_photos = db.relationship('UnitVentilator', backref='photo')
#     dhw_photos = db.relationship('DHW', backref='photo')
#     appliance_photos = db.relationship('Appliance', backref='photo')
#     building_photos = db.relationship('Building', backref='photo')
#     light_photos = db.relationship('Light', backref='photo')
#     exteriorwall_photos = db.relationship('ExteriorWall', backref='photo')
#     roof_photos = db.relationship('Roof', backref='photo')
#     rooffinish_photos = db.relationship('RoofFinish', backref='photo')
#     foundation_photos = db.relationship('Foundation', backref='photo')




@clientcommercial.route('/upload_image/', methods=['GET', 'POST'])
@login_required
def upload_file():
    if(current_user.is_authenticated and current_user.is_client()):
        form = UploadForm()
        if form.validate_on_submit():
            for filename in request.files.getlist('photo'):
                str_name='admin' + str(int(time.time()))
                name = hashlib.md5(str_name.encode("utf-8")).hexdigest()[:15]
                photos.save(filename, name=name + '.')

            success = True
        else:
            success = False
        return render_template('photo.html', form=form, success=success)
    else:
        abort(403)

@clientcommercial.route('/manage')
@login_required
def manage_file():
    if(current_user.is_authenticated and current_user.is_client()):
        files_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
        return render_template('manage.html', files_list=files_list)
    else:
        abort(403)

@clientcommercial.route('/open/<filename>')
@login_required
def open_file(filename):
    if(current_user.is_authenticated and current_user.is_client()):
        file_url = photos.url(filename)
        return render_template('browser.html', file_url=file_url)
    else:
        abort(403)

@clientcommercial.route('/delete/<filename>')
@login_required
def delete_file(filename):
    if(current_user.is_authenticated and current_user.is_client()):
        file_path = photos.path(filename)
        os.remove(file_path)
        return redirect(url_for('commercial.manage_file'))
    else:
        abort(403)








# Validation lsits


@clientcommercial.route("/ValidationLists")
@login_required
def Validation_Lists():
    if(current_user.is_authenticated and current_user.is_client()):

        Building_Types = pd.read_excel("Validation_Lists\Building_Types.xlsx")

        Door_R_Valeus = pd.read_excel(
            "Validation_Lists\Door_R_Values.xlsx")

        Exterior_Wall_R_Values = pd.read_excel(
            "Validation_Lists\Exterior_Wall_R_Values.xlsx")

        Glass_SHGC = pd.read_excel(
            "Validation_Lists\Glass_SHGC.xlsx")

        Insulation_K_Values = pd.read_excel(
            "Validation_Lists\Insulation_K_Value.xlsx")

        Interior_Wall_R_Values = pd.read_excel(
            "Validation_Lists\Interior_Wall_R_Values.xlsx")

        Roof_Finish_R_Values = pd.read_excel(
            "Validation_Lists\Roof_Finish_R_Values.xlsx")

        Roof_R_Values = pd.read_excel(
            "Validation_Lists\Roof_R_Values.xlsx")

        Window_R_Values = pd.read_excel(
            "Validation_Lists\Window_R_Values.xlsx")
    else:
        abort(403)


from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)





@clientcommercial.route("/gen/<int:id>", methods=['GET', 'POST'])
@login_required
def gen_docx(id):
    if(current_user.is_authenticated and current_user.is_client()):
        building = Building.query.get(id)
        building_id = building.id
        client_id = building.client_id
        client = Client.query.get(client_id)
              #lights_query = Light.query.filter_by(building_id=building_id).with_entities(Light.area_id, Light.hours, Light.fixture_count,
         #           Light.fixture, Light.lamp, Light.wattage).all()


        template = 'Template_6.docx'
        client_name = client.company
        facility_address = building.address
        building_name = building.name
        building_squarefootage = building.square_footage

        light_fields = ['area_id','hours','fixture_count','fixture','lamp','wattage']
        lights_query = Light.query.filter_by(building_id=building_id).all()
        lights = json.dumps(lights_query, cls=AlchemyEncoder)
        light2 = json.loads(lights)

        dhw_fields = ['building_id', 'equipment_type', 'area_id', 'tag','quantity', 'manufacturer', 'model_number', 'serial_number', 'year_built', 'input_capacity', 'fuel_type', 'storage_volume', 'effciency', 'set_point','insulation_value','notes']
        dhw_query = DHW.query.filter_by(building_id=building_id).all()
        dhw = json.dumps(dhw_query,cls=AlchemyEncoder)
        dhw2 = json.loads(dhw)

        pump_fields = ['building_id','area_id','tag','manufacturer','model_number','serial_number','year_built','gpm','fuel_type','pressure','horsepower','rpm','volts','effciency']
        pump_query = Pump.query.filter_by(building_id = building_id).all()
        pump = json.dumps(pump_query,cls=AlchemyEncoder)
        pump2 = json.loads(pump)

        motor_fields =['building_id','area_id','tag','manufacturer','model_number','serial_number','year_built','horsepower','rpm','volts','cfm','effciency']
        motor_query = Motor.query.filter_by(building_id = building_id).all()
        motor = json.dumps(motor_query,cls=AlchemyEncoder)
        motor2 = json.loads(motor)

        steam_boiler_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        steam_boiler_query = Steam_Boiler.query.filter_by(building_id = building_id).all()
        steam_boiler = json.dumps(steam_boiler_query,cls=AlchemyEncoder)
        steam_boiler2 = json.loads(steam_boiler)

        hydronic_boiler_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        hydronic_boiler_query = Hydronic_Boiler.query.filter_by(building_id = building_id).all()
        hydronic_boiler = json.dumps(hydronic_boiler_query,cls=AlchemyEncoder)
        hydronic_boiler2 = json.loads(hydronic_boiler)

        furnace_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        furnace_query = Furnace.query.filter_by(building_id = building_id).all()
        furnace = json.dumps(furnace_query,cls=AlchemyEncoder)
        furnace2 = json.loads(furnace)

        unit_heater_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        unit_heater_query = UnitHeater.query.filter_by(building_id = building_id).all()
        unit_heater = json.dumps(unit_heater_query,cls=AlchemyEncoder)
        unit_heater2 = json.loads(unit_heater)

        gas_fired_heating_coil_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        gas_fired_heating_coil_query = GasFiredHeatingCoil.query.filter_by(building_id = building_id).all()
        gas_fired_heating_coil = json.dumps(gas_fired_heating_coil_query,cls=AlchemyEncoder)
        gas_fired_heating_coil2 = json.loads(gas_fired_heating_coil)

        heat_pump_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        heat_pump_query = HeatPump.query.filter_by(building_id = building_id).all()
        heat_pump = json.dumps(heat_pump_query,cls=AlchemyEncoder)
        heat_pump2 = json.loads(heat_pump)

        electric_rest_heating_coil_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        electric_rest_heating_coil_query = ElectricRestHeatingCoil.query.filter_by(building_id = building_id).all()
        electric_rest_heating_coil = json.dumps(electric_rest_heating_coil_query,cls=AlchemyEncoder)
        electric_rest_heating_coil2 = json.loads(electric_rest_heating_coil)

        infrared_heater_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        infrared_heater_query = InfraredHeater.query.filter_by(building_id = building_id).all()
        infrared_heater = json.dumps(infrared_heater_query,cls=AlchemyEncoder)
        infrared_heater2 = json.loads(infrared_heater)

        make_up_air_unit_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        make_up_air_unit_query = MakeUpAirUnit.query.filter_by(building_id = building_id).all()
        make_up_air_unit = json.dumps(make_up_air_unit_query,cls=AlchemyEncoder)
        make_up_air_unit2 = json.loads(make_up_air_unit)

        packaged_rtu_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        packaged_rtu_query = PackagedRTU.query.filter_by(building_id = building_id).all()
        packaged_rtu = json.dumps(packaged_rtu_query,cls=AlchemyEncoder)
        packaged_rtu2 = json.loads(packaged_rtu)

        chiller_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        chiller_query = Chiller.query.filter_by(building_id = building_id).all()
        chiller = json.dumps(chiller_query,cls=AlchemyEncoder)
        chiller2 = json.loads(chiller)

        mini_split_system_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        mini_split_system_query = MiniSplitSystem.query.filter_by(building_id = building_id).all()
        mini_split_system = json.dumps(mini_split_system_query,cls=AlchemyEncoder)
        mini_split_system2 = json.loads(mini_split_system)

        packaged_terminal_ac_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        packaged_terminal_ac_query = PackagedTerminalAC.query.filter_by(building_id = building_id).all()
        packaged_terminal_ac = json.dumps(packaged_terminal_ac_query,cls=AlchemyEncoder)
        packaged_terminal_ac2 = json.loads(packaged_terminal_ac)

        condensing_unit_system_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        condensing_unit_system_query = CondensingUnitSystem.query.filter_by(building_id = building_id).all()
        condensing_unit_system = json.dumps(condensing_unit_system_query,cls=AlchemyEncoder)
        condensing_unit_system2 = json.loads(condensing_unit_system)

        window_air_conditioner_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        window_air_conditioner_query = WindowAirConditioner.query.filter_by(building_id = building_id).all()
        window_air_conditioner = json.dumps(window_air_conditioner_query,cls=AlchemyEncoder)
        window_air_conditioner2 = json.loads(window_air_conditioner)


        #photo_fields = ['steam_boiler_photos','hydronic_boiler_photos','pump_photos','motor_photos','chiller_photos','furnace_photos','heatpump_photos','pipe_photos','ahu_photos','gasfiredheatingcoil_photos','electricrestheatingcoil_photos','windowairconditioner_photos','infraredheater_photo',
        #                'makeupairunit_photos','minisplitsystem_photos','condensingunitsystem_photos','pakagedrtu_photos','packagedterminalac_photos','selfcontainedahu_photos','unitheater_photos','unitventilator_photos','dhw_photos','appliance_photos','building_photos','light_photos']
        #photo_query = Photo.query.filter_by(building_id = building_id),all()
        #photo = json.dumps(photo_query,cls=AlchemyEncoder)
        #photo2 = json.loads(photo)

        target_file = BytesIO()
        template = DocxTemplate("Template_5.docx")
        context = {
            'client_name': client_name,
            'facility_address': facility_address,
            'building_name': building_name,
            'building_squarefootage': building_squarefootage,
            'light_contents': light2,
            'dhw_contents' : dhw2,
            'pump_contents' : pump2,
            'motor_contents' : motor2,
            'hvac_contents' : steam_boiler2,
            ##'hvac_contents' : hydronic_boiler2,
            ##'hvac_contents' : furnace2,
            ##'hvac_contents' : unit_heater2,
            ##'hvac_contents' : gas_fired_heating_coil2,
            ##'hvac_contents' : heat_pump2,
            ##'hvac_contents' : electric_rest_heating_coil2,
            ##'hvac_contents' : infrared_heater2,
            ##'hvac_contents' : make_up_air_unit2,
            ##'hvac_contents' : packaged_rtu2,
            ##'hvac_contents' : chiller2,
            ##'hvac_contents' : mini_split_system2,
            ##'hvac_contents' : packaged_terminal_ac2,
            ##'hvac_contents' : condensing_unit_system2,
            ##'hvac_contents' : window_air_conditioner2
            #'photo_contents' : photo2

        }  # gets the context used to render the document


        target_file = BytesIO()
        template.render(context)
        template.save(target_file)


        document = target_file
        document.seek(0)


        return send_file(
            document, mimetype='application/vnd.openxmlformats-'
            'officedocument.wordprocessingml.document', as_attachment=True,
            attachment_filename='invoice.docx')
    else:
        abort(403)






@clientcommercial.route("/test/<int:id>", methods=['GET', 'POST'])
@login_required
def test(id):
    if(current_user.is_authenticated and current_user.is_client()):
        building = Building.query.get(id)
        building_id = building.id
        client_id=building.client_id
        client = Client.query.get(client_id)
        dhw_fields = ['equipment_type', 'area_id', 'tag', 'manufacturer', 'model_number', 'serial_number', 'year_built', 'input_capacity', 'fuel_type', 'storage_volume', 'effciency']
        light_fields = ['area_id','hours','fixture_count','fixture','lamp','wattage']
        #lights_query = Light.query.filter_by(building_id=building_id).with_entities(Light.area_id, Light.hours, Light.fixture_count, Light.fixture, Light.lamp, Light.wattage).all()
        lights_query = Light.query.filter_by(building_id=building_id).all()
        dhw_query = DHW.query.filter_by(building_id=building_id).all()
        dhw = json.dumps(dhw_query,cls=AlchemyEncoder)
        dhw2 = json.loads(dhw)
        lights = json.dumps(lights_query, cls=AlchemyEncoder)
        light2 = json.loads(lights)

        pump_fields = ['building_id','area_id','tag','manufacturer','model_number','serial_number','year_built','gpm','fuel_type','pressure','horsepower','rpm','volts','effciency']
        pump_query = Pump.query.filter_by(building_id = building_id).all()
        pump = json.dumps(pump_query,cls=AlchemyEncoder)
        pump2 = json.loads(pump)

        motor_fields =['building_id','area_id','tag','manufacturer','model_number','serial_number','year_built','horsepower','rpm','volts','cfm','effciency']
        motor_query = Motor.query.filter_by(building_id = building_id).all()
        motor = json.dumps(motor_query,cls=AlchemyEncoder)
        motor2 = json.loads(motor)
        
        steam_boiler_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        steam_boiler_query = Steam_Boiler.query.filter_by(building_id = building_id).all()
        steam_boiler = json.dumps(steam_boiler_query,cls=AlchemyEncoder)
        steam_boiler2 = json.loads(steam_boiler)


        return str(light2 + dhw2 + motor2 + pump2 + steam_boiler2)
    else:
        abort(403)
if __name__ == "__main__":
    app.debug = True
    app.run()





# class ApplianceForm(FlaskForm):
#     appliance_type = SelectField('Type', choices=[('Air Conditioner','Air Conditioner'), 
#                  ('Air Ionizser','Air Ionizser'),
#                  ('Appliance Plug', 'Appliance Plug'), 
#                  ('Aroma Lamp', 'Aroma Lamp'), 
#                  ('Attic Fan', 'Attic Fan'),
#                  ('Bachelor Griller', 'Bachelor Griller'), 
#                  ('Bedside Lamp', 'Bedside Lamp'),
#                  ('Back Boiler', 'Back Boiler'), 
#                  ('Beverage Opener', 'Beverage Opener'), 
#                  ('Blender', 'Blender'),('Box fan','Box fan'),
#                  ('Box mangle','Box mangle'),
#                  ('Calculator','Calculator'),
#                  ('Camcorder','Camcorder'),
#                  ('Can opener','Can opener'),
#                  ('Cassette player','Cassette player'),
#                  ('Ceiling fan','Ceiling fan'),
#                  ('Central vacuum cleaner','Central vacuum cleaner'),
#                  ('Clock','Clock'),
#                  ('Grandfather clock','Grandfather clock'),
#                  ('Wall clock','Wall clock'),
#                  ('Clothes dryer','Clothes dryer'),
#                  ('Clothes iron','Clothes iron'),
#                  ('Coffee grinder','Coffee grinder'),
#                  ('Coffeemaker','Coffeemaker'),
#                  ('Coffee percolator','Coffee percolator'),
#                  ('Cold-pressed juicer','Cold-pressed juicer'),
#                  ('Cooler','Cooler'),
#                  ('Combo washer dryer','Combo washer dryer'),
#                  ('Computer','Computer'),
#                  ('Modem','Modem'),
#                  ('Mouse (computer)','Mouse (computer)'),
#                  ('Printer','Printer'),
#                  ('Keyboard','Keyboard'),
#                  ('Server','Server'),
#                  ('Convection oven','Convection oven'),
#                  ('Deep fryer','Deep fryer'),
#                  ('Dehumidifier','Dehumidifier'),
#                  ('Digital camera','Digital camera'),
#                  ('Dish drying cabinet','Dish drying cabinet'),
#                  ('Dishwasher','Dishwasher'),
#                  ('Drawer dishwasher','Drawer dishwasher'),
#                  ('DVD player','DVD player'),
#                  ('Edger','Edger'),
#                  ('Electric cooker','Electric cooker'),
#                  ('Electric razor','Electric razor'),
#                  ('Electric toothbrush','Electric toothbrush'),
#                  ('Electric water boiler','Electric water boiler'),
#                  ('Evaporative cooler','Evaporative cooler'),
#                  ('Exhaust hood','Exhaust hood'),
#                  ('Fan heater','Fan heater'),
#                  ('Desk fan','Desk fan'),
#                  ('Flame supervision device','Flame supervision device'),
#                  ('Food processor','Food processor'),
#                  ('Forced-air','Forced-air'),
#                  ('Freezer','Freezer'),
#                  ('Futon dryer','Futon dryer'),
#                  ('Garbage disposal unit','Garbage disposal unit'),
#                  ('Gas appliance','Gas appliance'),
#                  ('Gramaphone','Gramaphone'),
#                  ('Go-to-bed matchbox','Go-to-bed matchbox'),
#                  ('Hair dryer','Hair dryer'),
#                  ('Hair iron','Hair iron'),
#                  ('Hearing aid','Hearing aid'),
#                  ('Hob (hearth)','Hob (hearth)'),
#                  ('Home server','Home server'),
#                  ('Humidifier (Vaporizer)','Humidifier (Vaporizer)'),
#                  ('HVAC','HVAC'),
#                  ('Icebox','Icebox'),
#                  ('Juicer','Juicer'),
#                  ('Karaoke Set','Karaoke Set'),
#                  ('Microphone','Microphone'),
#                  ('Disco ball','Disco ball'),
#                  ('Kimchi refrigerator','Kimchi refrigerator'),
#                  ('Lawn mower','Lawn mower'),
#                  ('Riding mower','Riding mower'),
#                  ('Leaf blower','Leaf blower'),
#                  ('Lighter','Lighter'),
#                  ('Light fixture','Light fixture'),
#                  ('Mangle','Mangle'),
#                  ('Meat grinder','Meat grinder'),
#                  ('Megaphone','Megaphone'),
#                  ('Micathermic heater','Micathermic heater'),
#                  ('Microwave oven','Microwave oven'),
#                  ('Mixer','Mixer'),
#                  ('Mogul lamp','Mogul lamp'),
#                  ('Mousetrap','Mousetrap'),
#                  ('Nightlight','Nightlight'),
#                  ('Oil heater','Oil heater'),
#                  ('Oven','Oven'),
#                  ('Panini press','Panini press'),
#                  ('Pasta maker','Pasta maker'),
#                  ('Patio heater','Patio heater'),
#                  ('Paper shredder','Paper shredder'),
#                  ('Pencil sharpener','Pencil sharpener'),
#                  ('Popcorn maker','Popcorn maker'),
#                  ('Pressure-cooker','Pressure-cooker'),
#                  ('Radiator (heating)','Radiator (heating)'),
#                  ('Radio receiver','Radio receiver'),
#                  ('Refrigerator','Refrigerator'),
#                  ('Internet refrigerator','Internet refrigerator'),
#                  ('Thermal mass refrigerator','Thermal mass refrigerator'),
#                  ('Rotisserie','Rotisserie'),
#                  ('Sewing machine','Sewing machine'),
#                  ('Sink','Sink'),
#                  ('Kitchen sink','Kitchen sink'),
#                  ('Separate sink spray','Separate sink spray'),
#                  ('Slow cooker','Slow cooker'),
#                  ('Snowblower','Snowblower'),
#                  ('Space heater','Space heater'),
#                  ('Steam mop','Steam mop'),
#                  ('Stereo','Stereo'),
#                  ('Stove','Stove'),
#                  ('Sump pump','Sump pump'),
#                  ('Telephone','Telephone'),
#                  ('Digital Phone','Digital Phone'),
#                  ('Table lamp','Table lamp'),
#                  ('Television set','Television set'),
#                  ('Remote','Remote'),
#                  ('Speaker','Speaker'),
#                  ('Tie press','Tie press'),
#                  ('Toaster','Toaster'),
#                  ('Toaster oven','Toaster oven'),
#                  ('Trash compactor','Trash compactor'),
#                  ('Trouser press','Trouser press'),
#                  ('Vacuum cleaner','Vacuum cleaner'),
#                  ('Manual vacuum cleaner','Manual vacuum cleaner'),
#                  ('Robotic vacuum cleaner','Robotic vacuum cleaner'),
#                  ('Videocassette recorder','Videocassette recorder'),
#                  ('Waffle iron','Waffle iron'),
#                  ('Washing machine','Washing machine'),
#                  ('Water cooker','Water cooker'),
#                  ('Waterpik','Waterpik'),
#                  ('Water purifier','Water purifier'),
#                  ('Water heater','Water heater'),
#                  ('Solar water heater','Solar water heater'),
#                  ('Tankless water heater','Tankless water heater'),
#                  ('Weed Eater','Weed Eater'),
#                  ('Window fan','Window fan'),
#                  ('Air fryer','Air fryer'),
#                  ('Barbecue grill','Barbecue grill'),
#                  ('Beehive oven','Beehive oven'),
#                  ('Brasero (heater)','Brasero (heater)'),
#                  ('Brazier','Brazier'),
#                  ('Bread machine','Bread machine'),
#                  ('Burjiko','Burjiko'),
#                  ('Butane torch','Butane torch'),
#                  ('Chapati maker','Chapati maker'),
#                  ('Cheesemelter','Cheesemelter'),
#                  ('Chocolatera','Chocolatera'),
#                  ('Chorkor oven','Chorkor oven'),
#                  ('Clome oven','Clome oven'),
#                  ('Comal (cookware)','Comal (cookware)'),
#                  ('Combi steamer','Combi steamer'),
#                  ('Communal oven','Communal oven'),
#                  ('Convection microwave','Convection microwave'),
#                  ('Corn roaster','Corn roaster'),
#                  ('Crepe maker','Crepe maker'),
#                  ('Earth oven','Earth oven'),
#                  ('Energy regulator','Energy regulator'),
#                  ('Espresso machine','Espresso machine'),
#                  ('Field kitchen','Field kitchen'),
#                  ('Fire pot','Fire pot'),
#                  ('Flattop grill','Flattop grill'),
#                  ('Food steamer','Food steamer'),
#                  ('Fufu Machine','Fufu Machine'),
#                  ('Halogen oven','Halogen oven'),
#                  ('Haybox','Haybox'),
#                  ('Horno','Horno'),
#                  ('Hot box (appliance)','Hot box (appliance)'),
#                  ('Hot plate','Hot plate'),
#                  ('Instant Pot','Instant Pot'),
#                  ('Kamado','Kamado'),
#                  ('Kettle','Kettle'),
#                  ('Kitchener range','Kitchener range'),
#                  ('Kujiejun','Kujiejun'),
#                  ('Kyoto box','Kyoto box'),
#                  ('Makiyakinabe','Makiyakinabe'),
#                  ('Masonry oven','Masonry oven'),
#                  ('Mess kit','Mess kit'),
#                  ('Multicooker','Multicooker'),
#                  ('Pancake machine','Pancake machine'),
#                  ('Panini sandwich grill','Panini sandwich grill'),
#                  ('Pressure cooker','Pressure cooker'),
#                  ('Pressure fryer','Pressure fryer'),
#                  ('Reflector oven','Reflector oven'),
#                  ('Remoska','Remoska'),
#                  ('Rice cooker','Rice cooker'),
#                  ('Rice polisher','Rice polisher'),
#                  ('Roasting jack','Roasting jack'),
#                  ('Rocket mass heater','Rocket mass heater'),
#                  ('Rotimatic','Rotimatic'),
#                  ('Russian oven','Russian oven'),
#                  ('Sabbath mode','Sabbath mode'),
#                  ('Salamander broiler','Salamander broiler'),
#                  ('Samovar','Samovar'),
#                  ('Sandwich toaster','Sandwich toaster'),
#                  ('Self-cleaning oven','Self-cleaning oven'),
#                  ('Shichirin','Shichirin'),
#                  ('Solar cooker','Solar cooker'),
#                  ('Sous-vide cooker','Sous-vide cooker'),
#                  ('Soy milk maker','Soy milk maker'),
#                  ('Susceptor','Susceptor'),
#                  ('Tabun oven','Tabun oven'),
#                  ('Tandoor','Tandoor'),
#                  ('Tangia','Tangia'),
#                  ('Thermal immersion circulator','Thermal immersion circulator'),
#                  ('Toaster and toaster ovens','Toaster and toaster ovens'),
#                  ('Turkey fryer','Turkey fryer'),
#                  ('Vacuum fryer','Vacuum fryer'),
#                  ('Wet grinder','Wet grinder'),
#                  ('Wood-fired oven','Wood-fired oven')])
#     quantity = StringField('Quantity')
#     wattage = StringField('Wattage')
#     photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])
#     submit = SubmitField('Upload')
#     submitButton = SubmitField('Add')

# class LightForm(FlaskForm):
#      fixtures = StringField('Number of Fixtures')
#      hours = StringField('Hours')
#      fixture_type = SelectField('Fixtures Type', choices=[('troffer', 'Troffer'),('linear', 'Linear'),('potlight','Potlight'),('polelight','Polelight'),('highbay','Highbay'),('wallpack','Wallpack')])
#      lamp_type = SelectField('Lamp Type', choices=[('t8','T8'),('t5','T5'),('t12','T12'),('tubeled','Tubeled'),('led','LED'),('metalhalide','Metal Halide'),('highpressuresodium','High Pressure Sodium'),('cfl','CFL')])
#      wattage = StringField('Lamp Wattage')
#      lamps_per_fixture = StringField('Lamps Per Fixture')
#      lamp_count = StringField('Number of Lamps')
#      photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class AreaForm(FlaskForm):
#     name = StringField("Name")

# class SteamBoilerForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         input_capacity = StringField('Input Capacity')
#         output_capacity = StringField('Output Capacity')
#         heating_eff = StringField('Heating eff')
#         boiler_type = StringField('Boiler Type')
#         pressure = StringField('Pressure')     
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])
    
# class FurnaceForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         input_capacity = StringField('Input Capacity')
#         output_capacity = StringField('Output Capacity')
#         heating_eff = StringField('Heating eff')
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class HydronicBoilerForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         input_capacity = StringField('Input Capacity')
#         output_capacity = StringField('Output Capacity')
#         heating_eff = StringField('Heating eff')
#         boiler_type = StringField('Boiler Type')
#         lhwt = StringField('LHWT')
#         ehwt = StringField('EHWT')
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class UnitHeaterForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         input_capacity = StringField('Input Capacity')
#         output_capacity = StringField('Output Capacity')
#         heating_eff = StringField('Heating eff')
#         supply_air_temp = StringField("Supply Air Setpoint")
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class GasFiredHeatingCoilForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         input_capacity = StringField('Input Capacity')
#         output_capacity = StringField('Output Capacity')
#         heating_eff = StringField('Heating eff')
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class HeatPumpForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         fuel_type = StringField("Fuel Type")
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class ElectricRestHeatingCoilForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         input_capacity = StringField('Input Capacity')
#         output_capacity = StringField('Output Capacity')
#         heating_eff = StringField('Heating eff')
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class InfraredHeaterForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         input_capacity = StringField('Input Capacity')
#         output_capacity = StringField('Output Capacity')
#         heating_eff = StringField('Heating eff')
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class MakeUpAirUnitForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         cooling_capacity = StringField("Cooling Capacity")
#         cooling_coil_type = StringField("Cooling Coil Type")
#         compressor_type = StringField("Compressor Type")
#         heating_capacity = StringField("Heating Capacity")
#         heating_coil_type = StringField("Heating Coil Type")
#         heating_eff = StringField('Heating eff')
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])


# class PackagedRTUForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         compressor_type = StringField("Compressor Type")
#         cooling_capacity = StringField("Cooling Capacity")
#         refridgerant = StringField("Refridgerant")
#         kwton = StringField("KW/Ton")
#         eer = StringField("EER")
#         heating_capacity = StringField("Heating Capacity")
#         heating_coil_type = StringField("Heating Coil Type")
#         heating_eff = StringField('Heating eff')
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class ChillerForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         compressor_type = StringField("Compressor Type")
#         cooling_capacity = StringField("Cooling Capacity")
#         refridgerant = StringField("Refridgerant")
#         kwton = StringField("KW/Ton")
#         eer = StringField("EER")
#         chiller_type = StringField("Chiller Type")
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])


# class MiniSplitSystemForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         compressor_type = StringField("Compressor Type")
#         cooling_capacity = StringField("Cooling Capacity")
#         refridgerant = StringField("Refridgerant")
#         kwton = StringField("KW/Ton")
#         eer = StringField("EER")
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class PackagedTerminalACForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         compressor_type = StringField("Compressor Type")
#         cooling_capacity = StringField("Cooling Capacity")
#         refridgerant = StringField("Refridgerant")
#         kwton = StringField("KW/Ton")
#         eer = StringField("EER")
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class WindowAirConditionerForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         compressor_type = StringField("Compressor Type")
#         cooling_capacity = StringField("Cooling Capacity")
#         refridgerant = StringField("Refridgerant")
#         kwton = StringField("KW/Ton")
#         eer = StringField("EER")
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class CondensingUnitSystemForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         compressor_type = StringField("Compressor Type")
#         cooling_capacity = StringField("Cooling Capacity")
#         refridgerant = StringField("Refridgerant")
#         kwton = StringField("KW/Ton")
#         eer = StringField("EER")
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])


# class MotorForm(FlaskForm):
#         manufacturer = StringField('Manufacturer')
#         model_number = StringField('Model Number')
#         serial_number = StringField('Serial Number')
#         year_built = StringField('Year Built')
#         condition = StringField("Condition")
#         horsepower = StringField("Horsepower")
#         rpm = StringField("RPM")
#         effciency = StringField("Effciency")
#         volts = StringField("Volts")
#         bhp = StringField("BHP")
#         frame = StringField("Frame")
#         fla = StringField("FLA")
#         cfm = StringField("CFM")
#         phase = StringField("Phase")
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class PumpForm(FlaskForm):
#         condition = StringField("Condition")
#         head = StringField("Head")
#         gpm = StringField("GPM")
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class BuildingForm(FlaskForm):
#         building_name = StringField("Building Name")
#         address = StringField("Address")
#         city = StringField("City")
#         province = StringField("Province")
#         postal_code = StringField("Postal Code")
#         square_footage = StringField("Square Footage")
#         photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class DHWForm(FlaskForm):
#     equipment_type = SelectField("Equipment Type", choices = [('Storage Heater', 'Storage Heater'), ('Boiler','Boiler'),('Instantaneous','Instantaneous')])
#     tag = StringField("Tag")
#     manufacturer = StringField("Manufacturer")
#     model_number = StringField("Model Number")
#     serial_number = StringField("Serial Number")
#     input_capacity = StringField("Input Capacity")
#     fuel_type = SelectField("Fuel Type", choices = [('Natural Gas','Natural Gas'), ('Electricity', 'Electricity')])
#     efficiency = StringField("Efficieny")
#     storage_volume = StringField("Storage Volume")
#     set_point = StringField("Set Point")
#     photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])


# class ExteriorWallForm(FlaskForm):
#     material = SelectField("Material", choices = [('Brick Veneer','Brick Veneer'),('Coated Steel','Coated Steel'),('Concrete Block','Concrete Block'),('Fiberglass','Fiberglass'),('Fiberglass Paneling','Fiberglass Paneling'),('Limestone Block','Limestone Block'),('Poured Concrete','Poured Concrete'),('Steel Paneling','Steel Paneling'),('Stone Aggregate','Stone Aggregate'),('Stucco','Stucco'),('Vinyl Paneling','Vinyl Paneling'),('Wood','Wood'),('Wood Paneling','Wood Paneling')])
#     rvalue = SelectField("R Value", choices = [('1.20','1.20'),('0.61','0.61'),('1.28','1.28'),('2.00','2.00'),('1.00','1.00'),('0.96','0.96'),('1.28','1.28'),('0.61','0.61'),('1.00','1.00'),('0.12','0.12'),('1.80','1.80'),('2.80','2.80'),('2.80','2.80')])
#     photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class RoofForm(FlaskForm):
#     material = SelectField("Material", choices = [('Brick Veneer','Brick Veneer'),('Concrete Block','Concrete Block'),('Fiberglass Paneling','Fiberglass Paneling'),('Poured Concrete','Poured Concrete'),('Steel Paneling','Steel Paneling'),('Stone Aggregate','Stone Aggregate'),('Stucco','Stucco'),('Vinyl Paneling','Vinyl Paneling'),('Wood Paneling','Wood Paneling')])
#     rvalue = SelectField("R Value", choices = [('1.20','1.20'),('1.28','1.28'),('1.00','1.00'),('1.28','1.28'),('0.61','0.61'),('1.00','1.00'),('0.12','0.12'),('0.90','0.90'),('2.80','2.80')])
#     photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class RoofFinishForm(FlaskForm):
#     material = SelectField("Material", choices = [('None','None'),('Asphalt Shingles','Asphalt Shingles'),('Bitumen','Bitumen'),('Clay Tiles','Clay Tiles'),('Concrete Tiles','Concrete Tiles'),('Fiberglass Paneling','Fiberglass Paneling'),('Gravel','Gravel'),('Green Roof','Green Roof'),('Grit','Grit'),('Mineral','Mineral'),('Rubber','Rubber'),('Rubber UV Reflector','Rubber UV Reflector'),('Spanish Tiles','Spanish Tiles'),('Steel Paneling','Steel Paneling')])
#     rvalue = SelectField("R Value", choices = [('0.00','0.00'),('0.44','0.44'),('0.88','0.88'),('0.25','0.25'),('0.69','0.69'),('0.88','0.88'),('0.69','0.69'),('1.00','1.00'),('0.00','0.00'),('1.00','1.00'),('0.00','0.00'),('0.00','0.00'),('1.30','1.30'),('1.60','1.60'),('0.25','0.25'),('0.61','0.61')])
#     photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])

# class FoundationForm(FlaskForm):
#     foundation_type = SelectField("Foundation Type", choices = [('Slabs-On-Grade','Slabs-On-Grade'),('Raised Floor','Raised Floor'),('Basement','Basement')])
#     material = SelectField("Material", choices = [('Concrete','Concrete'),('Brick','Brick'),('Wood','Wood'),('Steel','Steel'),('Stone','Stone')])
#     rx = SelectField("RX", choices = [('2','2'),('0.5','0.5'),('1','1')])
#     rvalue = SelectField('R Value', choices = [('1.28','1.28'),('1.2','1.2'),('2.8','2.8'),('0.61','0.61'),('1','1')])
#     photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])


# class ClientForm(FlaskForm):
#     company = StringField("Comapny")
#     first_name = StringField("First Name")
#     last_name = StringField("Last Name")
#     email = StringField("Email")
#     address = StringField("Address")
#     postal_code = StringField("Postal Code")
#     province = StringField("Province")
#     photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])


# class UploadForm(FlaskForm):
#     photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])
#     submit = SubmitField('Upload')

#  