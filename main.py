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
        self.server = jsonrpclib.Server('http://{}:{}'.format(self.hostname, self.port))
        server = self.server
        
        
class MiddleServer
    def __getattr__(self, name) # Google about overriding getattr in python
        #One more server instance
        method = server.__getattr__(name)
        response = method()
        server.stop() #not sure if this is correct, testing required.

class DeviceControl():

    def GET(self):
        global server
        game_info = {'state':server.__getattr__("get_game_state")(), 'name':'Museum'}
        time_left = server.get_time_left()
        devices = server.get_devices()
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
                test_result = server.test_devices()
            except: #TODO: monitor for exceptions as they appear
                raise
            else:
                return devices
        else:
            pass #Maybe issue a warning?

class GameControl():

    def GET(self):
        
        print "#"
        while True:
            try:
                print "##"
                game_info = {'state':server.get_game_state(), 'name':'Museum'}
                break
            except:
                print "###"
                sleep(1)
                pass
        
        print "#!"
        #game_info = {'state':server.get_game_state(), 'name':'Museum'}
        time_left = server.get_time_left()
        steps = server.get_steps()
        #Modifying steps for nice UI output
        step_num_dict = {}
        for index, step in enumerate(steps): 
            step['number'] = index + 1 #Assigning numbers to steps for the UI
            step_num_dict[step['name']] = step['number'] #Making step_name:step_number mappings
        for index, step in enumerate(steps): #Doing a second pass to ensure all the mappings we need are there
            step['stepnum_that_enable'] = [str(step_num_dict[step_name]) for step_name in step['steps_that_enable'] if step_name != 'start'] #An exception: 'start' step is not an actual step
            if not step['stepnum_that_enable']:
                 step['stepnum_that_enable'] = ["Start"]
        return render.game(game_info, time_left, steps)

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
                steps = server.get_steps()
                step_name = steps[step_index]['name']
            except KeyError:
                raise
            
            print "2#"
            while True:
                try:
                    print "2##"
                    server.enable_step(step_name)
                    break
                except:
                    print "2###"
                    sleep(1)
                    pass
            print "2#!"
                    
            
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
        '/steps', 'GameControl'
        #'/devices', 'DeviceControl'
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
