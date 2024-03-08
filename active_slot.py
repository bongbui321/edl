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


if __name__ == "__main__":
  main()
