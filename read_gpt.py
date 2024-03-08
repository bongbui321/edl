from binascii import hexlify
def main():
  with open("/home/bongb/bongbui321_gpt_dump_a/gpt_main0.bin", "rb") as f:
    for line in f:
      print(hexlify(line[4096: 4096+92]))

if __name__ == "__main__":
  main()