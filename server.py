import web
import jsonrpclib
import gettext

import os
import sys
import logging
import config

from time import sleep

# i18n directory.
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'i18n')

server = None #Ugly hack with globals, need to think of better way to store the variable

class ConnectionManager():

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.server = None

    def start_server(self):
        global server
        server = MiddleServer()
        
        
class MiddleServer():
    def __getattr__(self, name): # Google about overriding getattr in python
        server = jsonrpclib.Server('http://{}:{}'.format('localhost', 8070))
        method = server.__getattr__(name)
        return method
 

class DeviceControl():

    def GET(self):
        global server
        game_info = {'state':server.__getattr__("get_game_state")(), 'name':'Museum'}
        time_left = server.get_time_left()
        devices = server.get_devices()
        print(devices)
        return render.devices(game_info, devices)

    def POST(self):
        post_data = web.input()
        print(post_data)
        try:
            action = post_data['action']
        except KeyError:
            return False
        if action == 'get_devices':
            try:
                devices = server.get_devices()
            except: #TODO: monitor for exceptions as they appear
                raise
            else:
                return devices
        elif action == 'test_devices':
            try:
                test_result = MiddleServer.__getAttr__("test_devices")()
            except: #TODO: monitor for exceptions as they appear
                raise
            else:
                return devices
        else:
            pass #Maybe issue a warning?
        
class DebugPage():

    def GET(self):
        global server
        game_info = {'state':server.__getattr__("get_game_state")(), 'name':'Museum'}
        time_left = server.get_time_left()
        problem_list = ["No Skittles left", "Sensor not found", "Everything is on fire"]
        return render.debug(problem_list)

    def POST(self):
        post_data = web.input()
        print(post_data)
        try:
            action = post_data['action']
        except KeyError:
            return False
        if action == 'restart_server':
            try:
                devices = server.get_devices()
            except: #TODO: monitor for exceptions as they appear
                raise
            else:
                return devices
        elif action == 'test_devices':
            try:
                test_result = MiddleServer.__getAttr__("test_devices")()
            except: #TODO: monitor for exceptions as they appear
                raise
            else:
                return devices
        else:
            pass #Maybe issue a warning?
        

class GameControl():

    def GET(self):
        game_info = {'state':server.__getattr__("get_game_state")(), 'name':'Museum'}
        time_left = server.__getattr__("get_time_left")()
        steps = server.__getattr__("get_steps")()
        #Modifying steps for nice UI output
        step_num_dict = {}
        for index, step in enumerate(steps): 
            step['number'] = index + 1 #Assigning numbers to steps for the UI
            step_num_dict[step['name']] = step['number'] #Making step_name:step_number mappings
        for index, step in enumerate(steps): #Doing a second pass to ensure all the mappings we need are there
            step['stepnum_that_enable'] = [str(step_num_dict[step_name]) for step_name in step['steps_that_enable'] if step_name != 'start'] #An exception: 'start' step is not an actual step
            if not step['stepnum_that_enable']:
                 step['stepnum_that_enable'] = ["Start"]

        return render.game(game_info, time_left, steps) #game info State is failing, check what's in there

    def POST(self):
        post_data = web.input()
        print(post_data)
        try:
            action = post_data['action']
        except KeyError:
            return False
        if action == 'finish_step':
            try:
                step_id = post_data["step_name"] 
                step_index = step_id[5:]
                step_index = int(step_index)-1
                steps = server.get_steps()
                step_name = steps[step_index]['name']
            except KeyError:
                raise
            try:
                server.finish_step(step_name)
            except: #TODO: monitor for exceptions as they appear
                raise
        elif action == 'enable_step':
            try:
                step_id = post_data["step_name"] 
                step_index = step_id[5:]
                step_index = int(step_index)-1
                steps = server.__getattr__("get_steps")()
                step_name = steps[step_index]['name']
            except KeyError:
                raise
            
            try: #TODO any reason for this to be separate from above try? KeyError reasons?
                server.enable_step(step_name)
            except:
                raise
                                
            
            #try:
            #    server.enable_step(step_name)
            #except: #TODO: monitor for exceptions as they appear
            #    raise
        elif action == 'start':
            try:
                len_minutes = post_data["minutes"] #Length, for now only minutes are supported
            except KeyError:
                len_minutes = 60
            try:
                p_count = post_data["p_count"] #Participant count
            except KeyError:
                p_count = 1
            try:
                server.start_game(p_count, len_minutes*60)
            except: #TODO: monitor for exceptions as they appear
                raise
        elif action == 'stop':
            try:
                server.stop_game()
            except: #TODO: monitor for exceptions as they appear
                raise
        elif action == 'get_time':
            try:
                return {"time_left":server.get_time_left()}
            except: #TODO: monitor for exceptions as they appear
                raise
        elif action == 'decrease_t':
            try:
                seconds = post_data["seconds"] 
            except KeyError:
                seconds = 0
            try:
                server.decrease_time(seconds)
            except: #TODO: monitor for exceptions as they appear
                raise
        elif action == 'increase_t':
            try:
                seconds = post_data["seconds"] 
            except KeyError:
                seconds = 0
            try:
                server.increase_time(seconds)
            except: #TODO: monitor for exceptions as they appear
                raise
        else:
            pass #Maybe issue a warning?

"""actions = {
"Stress test":server.stress_test,
}"""

if __name__ == "__main__":
    urls = (
        '/', 'GameControl',
        '/steps', 'GameControl',
        '/debug', 'DebugPage'
    )
    app = web.application(urls, globals())
    #gettext.install('messages', localedir, unicode=True)   
    #gettext.translation('messages', localedir, languages=['lv_LV']).install(True)  
    #render = web.template.render('templates/', globals={'_': _})
    render = web.template.render('templates/')
    app.internalerror = web.debugerror
    conn_manager = ConnectionManager('localhost', 8070)
    print("Starting server...")
    conn_manager.start_server()
    print("Starting game...")
    app.run()
