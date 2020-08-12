import os
import configparser
from re import search

class configFileIni():

    def read_whole_config_file(self):

        with open("config.ini") as f:
            config = f.read()
            f.close()
            return config

    def read_conf_file(self,section_name,parameter_name,key = None):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read("config.ini")
        if key is not None:
            if config.has_option(section_name,parameter_name):
                value = config.get(section_name,parameter_name)
                if value == key:
                    return True
                else:
                    return False
            else:
                return False
        if key is None:
            if config.has_option(section_name,parameter_name):
                value = config.get(section_name,parameter_name)
                if value is not None:
                    return (value)
                else:
                    return None
            else:
                return None

    def delete_section(self , section_to_delete):
        parser_search = configparser.ConfigParser()
        with open('config.ini', 'r+') as s:
            parser_search.readfp(s)
            parser_search.remove_section(section_to_delete)
            s.seek(0)
            parser_search.write(s)
            s.truncate()
            #print ('section %s deleted' %(section_to_delete) )

    def delete_option(self , section,option_to_delete):
        parser = configparser.ConfigParser()
        with open('config.ini', 'r+') as s:
            parser.readfp(s)
            parser.remove_option(section, option_to_delete)
            s.seek(0)
            parser.write(s)
            s.truncate()
            print ('option %s deleted' %(option_to_delete) )

    def get_secton_values(self , section_name_to_get):
        parser = configparser.ConfigParser()
        parser.read('config.ini')
        list_str = []
        for section_name in parser.sections():
            if  search(section_name_to_get ,section_name):
                #list_str.append(section_name)
                # str = '%s '  %(section_name)
                for name, value in parser.items(section_name):
                #     str += ( '%s=%s ' % (name, value))
                 list_str.append(value)
        #print(list_str)
        return (list_str)

    def get_secton_name(self , section_name_to_get):
        parser = configparser.ConfigParser()
        parser.read('config.ini')
        list_str = []
        for section_name in parser.sections():
            if  search(section_name_to_get ,section_name):
                list_str.append(section_name)
                # str = '%s '  %(section_name)
                #for name, value in parser.items(section_name):
                #     str += ( '%s=%s ' % (name, value))
                # list_str.append(value)
        #print(list_str)
        return (list_str)

    def get_all_clients(self):
        parser = configparser.ConfigParser()
        parser.read('config.ini')
        list_str = []
        for section_name in parser.sections():
            if  search("Client*" ,section_name):
                str = '%s '  %(section_name)
                for name, value in parser.items(section_name):
                    str += ( '%s=%s ' % (name, value))
                list_str.append([str.__str__()])
        return (list_str)




    def write_to_conf_file(self,params_list):
        configfile_name = "config.ini"
        if os.path.isfile(configfile_name):
            pass
        else:
            print("config file not exist")
            sys.exit(1)
        cfgfile = open(configfile_name, 'a')
        Config = configparser.ConfigParser()
        list_section_name = []


        for param in params_list:
            section_name = param[0]
            if self.get_secton_name(section_name) is not None:
                self.delete_section(section_name)



        for param in params_list:
            section_name = param[0]
            parameter_name = param[1]
            key = param[2]

            if section_name != "" and parameter_name != "" and key != "" :
                if section_name not in list_section_name:
                    list_section_name.append(section_name)
                    Config.add_section(section_name)
                Config.set(section_name, parameter_name, key)
        Config.write(cfgfile)
        cfgfile.close()




