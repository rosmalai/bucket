import os
import cmd
import json
import datetime

class TextTrackerCli(cmd.Cmd):
    prompt = 'TaskatrackerCli>>'
    intro = 'Welcome to the TaskTrackerCli. Type"help" for available commands.'

    def __init__(self):
        super().__init__()
        self.task_file = 'task.json'
        self.tasks = self.load_tasks()

    # load the tasks from the json file
    def load_tasks(self):
        if not os.path.exists(self.task_file):
            # create an empty task list if file doesn't exists
            with open(self.task_file, 'w') as f:
                json.dump([], f)
            return []
        try:
            with open(self.task_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # return empty list if file is corrupted
            return []

    # save the task in the json file
    def save_task(self):
        with open(self.task_file, "w") as f:
            json.dump(self.tasks, f, indent=4)

    ''''''
    # print hello
    def do_hello(self, line):
        print("Hello")
    ''''''     
    
    def do_add(self, line):
        new_id = len(self.tasks) + 1
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if line:
            task = {
                'id': new_id,
                'description': line.strip(),
                'status': "todo", # todo/in-progress/done
                'createdAt': current_time,
                'updatedAt': current_time  
            }
            self.tasks.append(task)
            self.save_task()
            print(f"Task added: {line}")

    def do_update(self, line):
        '''Usage: update <id> <description> 
                  <status> <id>'''
        args = line.split(maxsplit=1)
        if len(args)!=2:
            print("Error: Please provide both Id and task")
            print("Usage: update <id> <description>")
            return 
        
        task_id = int(args[0])
        new_description = args[1].strip()

        for task in self.tasks:
            if task['id'] == task_id:
                task['description'] = new_description
                task['updatedAt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_task()
                print(f"Task {task_id} updated: {new_description}")
                return
        print(f"Error: Task with ID {task_id} not found")

    def do_delete(self, line):
        if not line:
            print("Error: Provide a task ID")
            return
        try:
            task_id = int(line)
            for index, task in enumerate(self.tasks):
                if task['id'] == task_id:
                    removed_task = self.tasks.pop(index)
                    self.save_task()
                    print(f"Task {task_id} deleted: {removed_task['description']}")
                    return
            print(f"Error: Task with ID {task_id} not found")
        except ValueError:
            print("Error: Task ID must be a number")

    def do_mark_in_progress(self, line):
        if not line:
            print("Please provide a task ID")
            print("Usage: mark_in_progress")
            return
        
        try:
            task_id = int(line)
            for task in self.tasks:
                if task['id'] == task_id:
                    task['status'] = "in-prograss"
                    task['updatedAt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_task()
                    print(f"Task {task_id} marked as in-prograss: {task['description']} ")
                    return
            print(f"Error: Task with ID {task_id} not found")
        except ValueError:
            print("Task ID must be a number")

    
    def do_mark_done(self, line):
        if not line:
            print("Please provide a task ID")
            print("Usage: mark_done")
            return
        
        try:
            task_id = int(line)
            for task in self.tasks:
                if task['id'] == task_id:
                    task['status'] = "done"
                    task['updatedAt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_task()
                    print(f"Task {task_id} marked as done: {task['description']} ")
                    return
            print(f"Error: Task with ID {task_id} not found")
        except ValueError:
            print("Task ID must be a number")

    def do_list(self, line):
        if not self.tasks:
            print("No task found. ")
            return 
        
        print("\nAll tasks:")
        print("-" * 60)
        for task in self.tasks:
            print(f"ID: {task['id']}")
            print(f"Description: {task['description']}")
            print(f"Status: {task['status']}")
            print(f"Created: {task['createdAt']}")
            print(f"Updated: {task['updatedAt']}")
            print("-" * 60)

    def do_list_done(self, line):
        if not self.tasks:
            print("No task found. ")
            return 
        
        print("\nAll completed tasks:")
        print("-" * 60)
        for task in self.tasks:
            if task['status'] == "done":
                print(f"ID: {task['id']}")
                print(f"Description: {task['description']}")
                print(f"Status: {task['status']}")
                print(f"Created: {task['createdAt']}")
                print(f"Updated: {task['updatedAt']}")
                print("-" * 60)

    # list all tasks to do
    def do_list_todo(self):
        if not self.tasks:
            print("No task found. ")
            return 
        
        print("\nAll completed tasks:")
        print("-" * 60)
        for task in self.tasks:
            if task['status'] == "todo":
                print(f"ID: {task['id']}")
                print(f"Description: {task['description']}")
                print(f"Status: {task['status']}")
                print(f"Created: {task['createdAt']}")
                print(f"Updated: {task['updatedAt']}")
                print("-" * 60)

    # list all tasks iin progress
    def do_list_in_progress(self):

        if not self.tasks:
            print("No task found. ")
            return 
        
        print("\nAll completed tasks:")
        print("-" * 60)
        for task in self.tasks:
            if task['status'] == "in-progress":
                print(f"ID: {task['id']}")
                print(f"Description: {task['description']}")
                print(f"Status: {task['status']}")
                print(f"Created: {task['createdAt']}")
                print(f"Updated: {task['updatedAt']}")
                print("-" * 60)

    # help user in command or something 
    def do_help(self, line):
        print("Add task: add <task>")
        
        print("Exit Terminal : quit")

    # exit terminal
    def do_quit(self, line):
        return True

if __name__ == "__main__":
    TextTrackerCli().cmdloop()