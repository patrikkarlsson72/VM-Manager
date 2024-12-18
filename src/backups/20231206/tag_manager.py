class TagManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.tags = set()  # Store tags in a set for uniqueness
        self.machine_tags = {}  # Store machine-tag assignments
        
        # Load existing tags and machine assignments
        self.tags = set(self.file_manager.load_tags())
        self.machine_tags = self.file_manager.load_machine_tags()

    def add_tag(self, tag_name: str) -> bool:
        """Add a new tag"""
        if not tag_name or tag_name in self.tags:
            return False
        self.tags.add(tag_name)
        self.file_manager.save_tags(list(self.tags))
        return True

    def remove_tag(self, tag_name: str) -> bool:
        """Remove a tag and all its assignments"""
        if tag_name not in self.tags:
            return False
        
        # Remove tag from set
        self.tags.remove(tag_name)
        
        # Remove tag from all machines
        for machine in self.machine_tags:
            if tag_name in self.machine_tags[machine]:
                self.machine_tags[machine].remove(tag_name)
        
        # Save changes
        self.file_manager.save_tags(list(self.tags))
        self.file_manager.save_machine_tags(self.machine_tags)
        return True

    def get_all_tags(self) -> set:
        """Get all existing tags"""
        return self.tags.copy()

    def get_machine_tags(self, machine_name: str) -> list:
        """Get all tags for a specific machine"""
        return self.machine_tags.get(machine_name, [])

    def add_machine_tag(self, machine_name: str, tag_name: str) -> bool:
        """Assign a tag to a machine"""
        if tag_name not in self.tags:
            return False
            
        if machine_name not in self.machine_tags:
            self.machine_tags[machine_name] = []
            
        if tag_name not in self.machine_tags[machine_name]:
            self.machine_tags[machine_name].append(tag_name)
            self.file_manager.save_machine_tags(self.machine_tags)
            return True
        return False

    def remove_machine_tag(self, machine_name: str, tag_name: str) -> bool:
        """Remove a tag from a machine"""
        if (machine_name in self.machine_tags and 
            tag_name in self.machine_tags[machine_name]):
            self.machine_tags[machine_name].remove(tag_name)
            self.file_manager.save_machine_tags(self.machine_tags)
            return True
        return False

    def get_machines_by_tags(self, tags: list) -> list:
        """Get all machines that have ALL the specified tags"""
        result = []
        for machine, machine_tags in self.machine_tags.items():
            if all(tag in machine_tags for tag in tags):
                result.append(machine)
        return result