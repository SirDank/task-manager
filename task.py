import os
import sys
from colorama import init, Fore, Style

def colorize(string):                                                             # colors!
    
    colorized = string
    white = Fore.WHITE + Style.BRIGHT
    green = Fore.GREEN + Style.BRIGHT
    to_colorize = ['[',']','>','<','-','.','#',':','"']
    for char in to_colorize:
        colorized = colorized.replace(char,f"{green}{char}{white}")
    return colorized

def filter_sort(sorted):                                                          # remove empty items from list and sort
    sorted = list(filter(None, sorted))
    sorted.sort()
    return sorted

def main(pos1, pos2, pos3):
    
    os.system('cls')
    tasks_dat = open("tasks.dat","r").read().splitlines()                         # reading tasks.dat
    if "TASKS=|" in tasks_dat[0]:
        tasks_dat[0] = tasks_dat[0].replace("TASKS=|","TASKS=")                   # auto-fix error-check
    if "DONE=|" in tasks_dat[1]:
        tasks_dat[1] = tasks_dat[1].replace("DONE=|","DONE=")                     # auto-fix error-check
    if "DELETED=|" in tasks_dat[2]:
        tasks_dat[2] = tasks_dat[2].replace("DELETED=|","DELETED=")               # auto-fix error-check

    def save_dat():                                                               # save tasks.dat
        open("tasks.dat","w").write('\n'.join(tasks_dat))

    if pos1 == "add":
        
        if pos2 == "" or pos3 == "" or not pos2.isdigit():                        # error-check
            print(colorize("\n  > Usage: task.bat add <PRIORITY> \"<TASK>\"\n  > Example: task.bat add 1 GDC.NET\n  > Example: task.bat add 2 \"hello world\""))
            return
        
        task_string = tasks_dat[0]
        pos2 = float(pos2)
        while f"{pos2}:" in task_string:
            pos2 = round(pos2 + 0.1,2)
            
        counter = 3
        while True:                                                              # gather additional text
            try:
                extra = sys.argv[counter]
                if extra != pos3:
                    pos3 += f" {extra}"
            except:break
            counter += 1
        
        tasks_dat[0] += f"{pos2}:{pos3}|"
        save_dat()
        print(colorize(f"\n  > Added Task: \"{pos3}\" with priority {pos2}"))

    elif pos1 == "rem":
        
        if pos2 == "" or not pos2.isdigit():                                    # error-check
            print(colorize("\n  > Usage: task.bat rem <INDEX>\n  > Example: task.bat rem 1"))
            return
        
        task_list = tasks_dat[0].replace("TASKS=","").split("|")
        task_list = filter_sort(task_list)
        if len(task_list) == 0:                                                 # error-check
            print(colorize("\n  > There are currently no tasks!"))
            return
        elif len(task_list) < int(pos2):                                        # error-check
            print(colorize(f"\n  > Task #{pos2} does not exist!"))
            return
        deleted_string = tasks_dat[2]
        
        task = task_list[int(pos2)-1]
        task_list.remove(task)
        deleted_string += task + '|'
 
        tasks_dat[0] = "TASKS=" + '|'.join(task_list) + '|'
        tasks_dat[2] = deleted_string
        save_dat()
        print(colorize(f"\n  > Deleted Task: #{pos2} [ {task.split(':')[1]} [{task.split(':')[0]}] ]"))
        
    elif pos1 == "done":
        
        if pos2 == "" or not pos2.isdigit():                                   # error-check
            print(colorize("\n  > Usage: task.bat done <INDEX>\n  > Example: task.bat done 1"))
            return
        
        task_list = tasks_dat[0].replace("TASKS=","").split("|")
        task_list = filter_sort(task_list)
        if len(task_list) == 0:                                               # error-check
            print(colorize("\n  > There are currently no tasks!"))
            return
        elif len(task_list) < int(pos2):                                      # error-check
            print(colorize(f"\n  > Task #{pos2} does not exist!"))
            return
        done_string = tasks_dat[1]
        
        task = task_list[int(pos2)-1]
        task_list.remove(task)
        done_string += task + '|'

        tasks_dat[0] = "TASKS=" + '|'.join(task_list) + '|'
        tasks_dat[1] = done_string
        save_dat()
        print(colorize(f"\n  > Completed Task: #{pos2} [ {task.split(':')[1]} [{task.split(':')[0]}] ]"))
        
    elif pos1 == "list":
        
        task_list = tasks_dat[0].replace("TASKS=","").split("|")
        task_list = filter_sort(task_list)
        counter = 1
        to_print = f"\n  > Pending : {len(task_list)}\n"
        
        for combo in task_list:
            priority, task = combo.split(":")
            to_print += f"  - {counter}. {task} [{priority}]\n"
            counter += 1
        
        print(colorize(to_print))
        
    elif pos1 == "report":
        
        task_list = tasks_dat[0].replace("TASKS=","").split("|")
        task_list = filter_sort(task_list)
        done_list = tasks_dat[1].replace("DONE=","").split("|")
        done_list = list(filter(None, done_list))
        deleted_list = tasks_dat[2].replace("DELETED=","").split("|")
        deleted_list = list(filter(None, deleted_list))
        
        counter = 1
        to_print = f"\n  > Pending : {len(task_list)}\n"
        for combo in task_list:
            priority, task = combo.split(":")
            to_print += f"  - {counter}. {task} [{priority}]\n"
            counter += 1
            
        counter = 1
        to_print += f"\n  > Completed : {len(done_list)}\n"
        for combo in done_list:
            priority, task = combo.split(":")
            to_print += f"  - {counter}. {task} [{priority}]\n"
            counter += 1
            
        counter = 1
        to_print += f"\n  > Deleted : {len(deleted_list)}\n"
        for combo in deleted_list:
            priority, task = combo.split(":")
            to_print += f"  - {counter}. {task} [{priority}]\n"
            counter += 1
            
        print(colorize(to_print))
        
    else:
        to_print = '''
  > Usage:- [ Windows ]
  - task.bat help                  # Displays this message
  - task.bat add 2 "hello world"   # Add a new item with priority 2 and text "hello world" to the list
  - task.bat rem <INDEX>           # Delete the incomplete item with the given index
  - task.bat done <INDEX>          # Mark the incomplete item with the given index as complete
  - task.bat list                  # Show incomplete priority list items sorted by priority in ascending order
  - task.bat report                # Display complete and incomplete tasks
        '''
        print(colorize(to_print))

if __name__ == "__main__":

    init(autoreset=True)
    os.chdir(os.path.dirname(__file__))                            # change dir to file location
    try:open("tasks.dat","x").write("TASKS=\nDONE=\nDELETED=\n")   # create tasks.dat to save stats
    except:pass

    try:pos1 = sys.argv[1].lower()   # get input position 1
    except:pos1 = ""
    try:pos2 = sys.argv[2]           # get input position 2
    except:pos2 = ""
    try:pos3 = sys.argv[3]           # get input position 3
    except:pos3 = ""
    
    main(pos1, pos2, pos3)           # start the program