#!/usr/bin/env python
"""
auto_mailer.py

A program that allows a CRON daemon to send automatic emails.
"""

SERVER_ADDRESS = "smtp.jhu.edu"
RETURN_ADDRESS = "harmsm@jhu.edu"

import smtplib, sys, time

class Email:

    def __init__(self,type,input_file):

        # Available types
        type_dict = {"gcf_snack":self.parseGCFSnack} 

        # Parse input file
        parse_status = type_dict[type](input_file)

        # If the parsing failes for some reason, email the owner
        if parse_status != 0:
            self.subj = "Failed auto email!"
            self.email_address = [RETURN_ADDRESS]
            self.body = "Auto send (type: %s, time: %s) failed!" % \
                        (type,time.asctime())
    
    def parseGCFSnack(self,snack_list):
        """
        Read the top name off of a snack list and prep and email reminder.

        Snack List Format:
        recip_name  recip_email  date
        """

        try:
            # Read in snack list
            f = open(snack_list,"r")
            recip_list = f.readlines()
            f.close()

            # Extract top line
            current_recip = recip_list.pop(0)
    
            # Write out list without top line
            g = open(snack_list,"w")
            g.writelines(recip_list)
            g.close()

            # Parse line
            col = current_recip.split()
            self.recip_name = col[0]
            self.email_address = [col[1],RETURN_ADDRESS]
            self.gcf_date = col[2]

        except (IndexError,OSError):
            return 1

        self.subj = "Feed the hungry! (GCF snacks)"
    
        msg = ["Hey %s!\n\n" % self.recip_name]
        msg.append("According to the copious records we keep here at GCF HQ, ")
        msg.append("you're up for snacks this week (%s).  " % self.gcf_date)
        msg.append("If you can't make it for some reason, reply to this email ")
        msg.append("and we'll make sure that the masses are somehow appeased.")
        msg.append("\n\n          --Your friendly neighborhood CRON daemon.")

        self.body = "".join(msg)

        return 0
    

    def sendMail(self):
        """
        Create a message using self.subj, self.body, and self.recip and send
        it.
        """
    
        message = "Subject: %s\n%s" % (self.subj,self.body)
        server = smtplib.SMTP(SERVER_ADDRESS)
        status = server.sendmail(RETURN_ADDRESS,self.email_address,message)
        server.close()

new_message = Email(sys.argv[1],sys.argv[2])
new_message.sendMail()

