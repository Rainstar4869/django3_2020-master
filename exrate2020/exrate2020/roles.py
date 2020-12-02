from rolepermissions.roles import AbstractUserRole


class Distributor(AbstractUserRole):
    role_name = "distributor"
    available_permissions = {
        'edit_member_discount_rate': True,
        'place_order': True,
    }


class Member(AbstractUserRole):
    role_name = "member"
    available_permissions = {
        'place_order': True,
    }
