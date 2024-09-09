import importlib

class SigilInfo:
	def __init__(self, sigil_id, name, scrybes, description, triggers, is_mox, is_conduit, is_active, has_mirror, can_stack):
        self.sigil_id = sigil_id
        self.name = name
        self.scrybes = scrybes
        self.description = description
        self.triggers = triggers
        self.effects = {}
        self.is_mox = is_mox
        self.is_conduit = is_conduit
        self.is_active = is_active
        self.has_mirror = has_mirror
        self.can_stack = can_stack
        # self.load_effects()