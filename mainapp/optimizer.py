import os
import random
import string


OPTIMIZE_REPEAT = True
REPEAT_SIZE = 3


class section:

    def __init__(self, selector, name, attribute_value):
        self.selector = selector
        self.name = name
        self.attribute_value = attribute_value  # dict type

    def __str__(self):
        data = self.selector+self.name+"{"
        for att in self.attribute_value.keys():
            data += att+":"+self.attribute_value[att]+";"
        data += "}\n"

        return data


class css_parser:

    file = None
    file_name = None
    file_size = 0

    new_file = None
    new_file_name = None

    old_size = None
    new_size = None
    percentage = 0

    separators = [".", "#", ":"]
    sections = []
    new_sections = []
    replace = []

    tags = ["*", "div", "h1", "h2", "section", "img", "form", "label", "select"]

    long_hand = [["border-radius", "border-style", "border-color"],
                 ["background-color", "background-image", "background-repeat", "background-position"]]
    short_hand = ["border", "background"]

    def __init__(self, file=None):
        if(not os.path.exists(file)):
            raise Exception("File not found")

        self.file = file
        self.file_name = file.split("/")[-1]
        self.file_size = self.size(self.file)

        self.analyser()
        self.short_hand_optimizer()
        self.repeater()
        self.size_optimizer()
        self.info()

    def analyser(self):
        data = ""
        with open(self.file, "r") as f:
            data = f.read()


        data_arr = [x for x in data.split("}") if x]

        #replace /n by empty char
        #since } is removed while splitting add it back
        for i in range(len(data_arr)):

            data_arr[i] += "}"
            data_arr[i] = data_arr[i].replace("\n", '')
            data_arr[i] = data_arr[i].replace(" ", '')

        #parse the data_arr items for section object
        for d in data_arr:

            #finding the separator
            selector_found = True
            if d[0] in self.separators:
                selector = d[0]
            else:
                selector_found = False

            #finding the var name
            if '{' not in d:
                print("Opening bracket ERROR AT:\n", d)
                raise Exception("Missing {")
            else:
                var_name = d.split('{')[0]

                if selector_found:
                    var_name = var_name.replace(selector, '')
                else:
                    if var_name in self.tags:
                        selector = ""
                    else:
                        print("ERROR AT:\n", d)
                        raise Exception("No such tags")

            #if selector not present then the var name must be a tag name
            if not selector_found:
                if var_name not in self.tags:
                    print("SEPARATOR ERROR AT:\n", d)
                    raise Exception("separator not found")

            #finding the attribute and value
            attribute_value = {}

            att_value = d.split('{')[1]
            att_value = att_value.split('}')[0]
            att_value = [x for x in att_value.split(';') if x]

            for i in att_value:
                prop = i.split(":")

                if len(prop) == 1:
                    print("ERROR AT:\n", d)
                    raise Exception("Missing :")
                else:
                    attribute_value[prop[0]] = prop[1]

            #create a section obj and append it in sections list
            sect = section(selector, var_name, attribute_value)
            self.sections.append(sect)

    def short_hand_optimizer(self):

        replace = []
        replacement = []

        for sect in self.sections:

            for i in range(len(self.long_hand)):  # detecting long hand

                count = 0
                rep = {}

                for j in range(len(self.long_hand[i])):
                    for att in sect.attribute_value:

                        val = sect.attribute_value[att]
                        if self.long_hand[i][j] == att:
                            count += 1
                            rep[att] = val

                if count > 1:
                    replace.append(rep)
                    replacement.append(self.short_hand[i])

        # for i in range(len(replace)):
        #     print(f"{replace[i]} -> {replacement[i]}")

    def get_random_class_name(self):
        c = ''.join(random.choices(string.ascii_uppercase +
                                   string.digits, k=7))

        for sect in self.sections:
            if sect.name == c:
                self.get_random_class_name()

        return c

    def repeater(self):

        count = {}

        for sect in self.sections:
            for att in sect.attribute_value:
                val = sect.attribute_value[att]
                if att in count.keys():
                    if val in count[att].keys():
                        count[att][val] = count[att][val]+1
                        if count[att][val] > REPEAT_SIZE:
                            self.replace.append(f"{att}:{val};")
                            if OPTIMIZE_REPEAT:
                                var_name = self.get_random_class_name()
                                attribute_value = {att: val}
                                new_sect = section(
                                    sect.selector, var_name, attribute_value)
                                self.new_sections.append(new_sect)
                                # print("adding...")
                                # print(new_sect)

                    else:
                        count[att][val] = 1
                else:
                    count[att] = {}
                    count[att][val] = 1

        # print("Duplicates Summary:")
        # print("=================\n\n\n")

        # for att in count.keys():
        #     for val in count[att].keys():
        #         if count[att][val] > REPEAT_SIZE:
        #             print(f"{att} : {val} -> {count[att][val]}")

    def size_optimizer(self):
        data = ""
        for sect in self.sections:
            data += str(sect)

        self.new_file_name = "size_optimized_"+self.file_name
        self.new_file = self.file.split("/")
        self.new_file.pop()
        # self.new_file += self.new_file_name
        self.new_file = "/".join(self.new_file)+"/"+self.new_file_name

        #optimize repeats
        if OPTIMIZE_REPEAT:
            for s in self.replace:
                data = data.replace(s, '')

        for sect in self.new_sections:
            data += str(sect)

        with open(self.new_file, "w") as f:
            f.write(data)


    def size(self, f):
        return os.path.getsize(f)

    def __str__(self):
        if(self.file):
            msg = "FILE: "+self.file+"\n"
            msg += "->FILE SIZE "+str(self.size(self.file))+" bytes\n"
            

            if self.new_file_name:
                msg += "FILE: "+self.new_file+"\n"
                msg += "->FILE SIZE " + \
                    str(self.size(self.new_file))+" bytes"+"\n"
                self.new_size = str(self.size(self.new_file))
                diff = self.size(self.file)-self.size(self.new_file)
                self.percenatge = diff/self.size(self.file)

                msg += "Space saved percentage = "+str(percenatge*100)+"\n"
        else:
            msg = "File not added"

        return msg

    def info(self):
        self.old_size = str(self.size(self.file))
        self.new_size = str(self.size(self.new_file))

        diff = self.size(self.file)-self.size(self.new_file)

        if self.size(self.file)!=0:
            self.percentage = round(diff/self.size(self.file)*100,2)
