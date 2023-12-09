# Here is the command args.
# We can use below commands to send to printer to do anything.
# Details using, Please refer to ../doc/developerDOC.pdf



test_page = "1B 3D 01 12 54"   # the command is Printing the test page
paper_in = "1A 0C 00"     # the command is pager in .
border = "1B 45 01 "
text = "1A 54 01 "      # Text printing command.
init_command = "1B 40 "  # printer init
start_page = "1A 5B 01 00 00 00 00 68 02 68 01 00"  # start to printing current page.
end_page = "1A 5D 00"   # the current page ended
printer = "1A 4F 00"    # enable printing
cut_paper = "1B 69"     # cut paper
print_qr = "1A 31 00 00 02 {} {} 00 {} 00 "  #print QR code.
reset_device = "1F 2D 52 00"  # reboot printer