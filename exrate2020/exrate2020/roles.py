from rolepermissions.roles import AbstractUserRole


class Distributor(AbstractUserRole):
    available_permissions = {
        'edit_member_discount_rate': True,
        'place_order': True,
    }


class Member(AbstractUserRole):
    available_permissions = {
        'place_order': True,
    }
