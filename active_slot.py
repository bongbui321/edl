from binascii import hexlify, unhexlify

AB_FLAG_OFFSET = 6
AB_PARTITION_ATTR_SLOT_ACTIVE = (0x1 << 2)
AB_PARTITION_ATTR_BOOT_SUCCESSFUL = (0x1 << 6)
AB_PARTITION_ATTR_UNBOOTABLE = (0x1 << 7)
AB_SLOT_ACTIVE_VAL = 0x3F
AB_SLOT_INACTIVE_VAL = 0x0
AB_SLOT_ACTIVE = 1
AB_SLOT_INACTIVE = 0
#['INFO: Calling handler for patch', 'INFO: Read Failed sector 4096, size 1 result 3']



def make_inactive(data_bytes):
  new_data = data_bytes
  new_data &= ~(AB_PARTITION_ATTR_SLOT_ACTIVE << 48)
  return new_data


def is_active(data):
  return (((data >> 48) & 0xff) & AB_PARTITION_ATTR_SLOT_ACTIVE) == AB_PARTITION_ATTR_SLOT_ACTIVE


def test_make_inactive(data):
  new_data = make_inactive(data)
  print(f"{hex(new_data)} is {'active' if is_active(new_data) else 'not active'}")
  return

PART_ATT_PRIORITY_BIT = 48
PART_ATT_ACTIVE_BIT = 50
PART_ATT_MAX_RETRY_CNT_BIT = 51
MAX_PRIORITY = 3
PART_ATT_SUCCESS_BIT = 54
PART_ATT_UNBOOTABLE_BIT = 55

PART_ATT_PRIORITY_VAL = 0x3 << PART_ATT_PRIORITY_BIT
PART_ATT_ACTIVE_VAL = 0x1 << PART_ATT_ACTIVE_BIT
PART_ATT_MAX_RETRY_COUNT_VAL = 0x7 << PART_ATT_MAX_RETRY_CNT_BIT
PART_ATT_SUCCESSFUL_VAL  = 0x1 << PART_ATT_SUCCESS_BIT
PART_ATT_UNBOOTABLE_VAL = 0x1 << PART_ATT_UNBOOTABLE_BIT

def set_boot_inactive(data):
  data &= (~PART_ATT_PRIORITY_VAL & ~PART_ATT_ACTIVE_VAL)
  data |= ((MAX_PRIORITY-1) << PART_ATT_PRIORITY_BIT)
  return data

def set_boot_active(data):
  data |= (PART_ATT_PRIORITY_VAL | PART_ATT_ACTIVE_VAL | PART_ATT_MAX_RETRY_COUNT_VAL)
  data &= (~PART_ATT_SUCCESSFUL_VAL) 
  data &= (~PART_ATT_UNBOOTABLE_VAL)
  return data


def main():
  a = 0x103d000000000000
  data_active = (a >> (AB_FLAG_OFFSET*8) & 0xff) & AB_PARTITION_ATTR_SLOT_ACTIVE 
  active = data_active == AB_PARTITION_ATTR_SLOT_ACTIVE
  print(f"0x{(a >> 48):04x}")
  print(f"0x{((a >> 48)&0xff):04x}")
  print(f"0x{(AB_PARTITION_ATTR_SLOT_ACTIVE):04x}")
  print(f"data_active: {data_active}")
  print(f"{str(a)} is {'active' if active else 'not active'}")

  b = 0x003b000000000000

  b_active = 0x103f000000000000
  a_active = 0x103d000000000000
  test_make_inactive(a_active)

  boot_active = 0x006f000000000000
  print(f"boot_flags to inactive:{set_boot_inactive(boot_active):02x}")

  boot_inactive = 0x003a000000000000
  print(f"boot_flags to active:{set_boot_active(boot_inactive):02x}")


if __name__ == "__main__":
  main()
