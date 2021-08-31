import os
import requests
import ftplib
from sys import stderr
from socket import gaierror


# TODO: in progress
class GetTool:
    def __init__(self):
        pass


class MyFTPTool:
    def __init__(self):
        while True:
            try:
                self.hostname = self.getHostName()
                print("Attempting to connect to {}".format(self.hostname))
                self.FtpCxn = ftplib.FTP(host=self.hostname)
                break
            except gaierror as e:
                print("Host: {} could not be found. Please try again.".format(self.hostname))

        print("**** Connection Successful! ****")
        self.login()

    # noinspection PyMethodMayBeStatic
    def getHostName(self):
        hn = input("Please Enter HostName [192.168.1.98]: ")
        if len(hn) > 0:
            return hn
        else:
            hn = "192.168.1.98"
            return hn

    def login(self):
        while True:
            try:
                print("**** Please Login to {} ****".format(self.hostname))
                if self.FtpCxn.login(input("User: "), input("Password: ")):
                    print(self.FtpCxn.getwelcome())
                    print("****** Login Successful! ******")
                    break
                else:
                    stderr.write("Login not successful, please try again.")
            except ftplib.error_perm as e:
                print(e)

    def _get_ftp_dir(self):
        print("\nAvailable files/folders in {} are: ".format(" '{}' ".format(self.FtpCxn.pwd())))
        for item in self.FtpCxn.nlst():
            print(item)

        while True:
            new_ftp_dir = input("Choose a new folder (press q to quit): ")
            if new_ftp_dir in self.FtpCxn.nlst("-d"):
                self.FtpCxn.cwd(new_ftp_dir)
                print("Current FTP Server directory is: {}".format(self.FtpCxn.pwd()))
                break

            elif new_ftp_dir.lower() == 'q':
                print("Ok, Quitting...")
                exit(0)

            elif not os.path.isdir(new_ftp_dir):
                print("folder '{}' not found, please try again".format(new_ftp_dir))

    def _ftp_dir_list(self):
        print("\nAvailable files/folders in {} are: ".format(" '{}' ".format(self.FtpCxn.pwd())))
        for item in self.FtpCxn.nlst():
            print(item)

    @staticmethod
    def _get_save_dir():
        while True:
            choice = input("Please choose location of the file to upload"
                           "\n or the save location for the downloaded file (or type default) (press q to quit): ")
            if choice == 'q':
                print("Ok, Quitting...")
                exit(0)

            elif choice == 'default':
                choice = '../Misc_Project_Files'
                print("defaulting to {}".format(choice))
                return choice

            elif os.path.isdir(choice):
                print("Folder validated")
                return choice

            elif not os.path.isdir(choice):
                print("Folder not detected, please try again.")

    def choose_file(self, transfer_type):
        self._ftp_dir_list()
        while True:
            change_dir_q = input("Would you like to change directories? (y/n or q to quit): ").lower()
            if change_dir_q == 'y':
                self._get_ftp_dir()
                break
            elif change_dir_q == 'n':
                break
            elif change_dir_q == 'q':
                print("Ok, Quitting...")
                exit(0)
            else:
                print("Please choose \'y\', \'n\', or press \'q\' to quit.")
        savedir = self._get_save_dir()
        os.chdir(savedir)

        self._ftp_dir_list()
        while True:
            if transfer_type == 'upload':
                filename = input("Please enter the name of the file to upload: ")
                if filename in os.listdir(savedir):
                    print("{} chosen".format(filename))
                    return filename
                else:
                    print("\'{}\' not found in, \'{}\' please try again.".format(filename, savedir))

            elif transfer_type == 'download':
                filename = input("Please enter the name of the file to download: ")
                if filename in self.FtpCxn.nlst():
                    print("{} chosen".format(filename))
                    return filename
                else:
                    print("\'{}\' not found in, \'{}\' please try again.".format(filename, self.FtpCxn.pwd()))

    def attempt_download(self, filename):
        try:
            with open(filename, 'wb') as localfile:
                self.FtpCxn.retrbinary('RETR ' + filename, localfile.write, 1024)
                print('File downloaded successfully!')
        except ftplib.Error as e:
            print("error encountered: {}".format(e))
            os.remove(filename)

    def upload_file_to_ftp(self, filename):
        self.FtpCxn.storbinary('STOR ' + filename, open(filename, "rb"))
        print("{} uploaded".format(filename))
        self.choose_ftp_func()

    def choose_ftp_func(self):
        function_choices = {1: "Upload",
                            2: "Download",
                            3: "Change Directory"}

        for c in function_choices:
            print(str(c) + ". " + function_choices[c])

        # choose function loop
        while True:
            choice = input("Please Enter the line number of the function "
                           "you would like to run (or press q to quit): ").lower()
            if choice == 'q':
                print("Ok, Quitting...")
                exit(0)
            elif int(choice) in function_choices.keys():
                if function_choices[int(choice)].lower() == 'download':

                    file_to_download = self.choose_file(transfer_type='download')
                    self.attempt_download(file_to_download)
                elif function_choices[int(choice)].lower() == "upload":
                    file_to_download = self.choose_file(transfer_type='upload')
                    self.upload_file_to_ftp(file_to_download)
                break
            else:
                print("Please choose a line number from the list above.")


class GetFileHttp:
    def __init__(self, url):
        self.r = requests.get(url)
        self.process_file()

    def _get_content_type(self):
        if (self.r.headers['Content-Type'] == 'text/html'
                or 'text' in self.r.headers['Content-Type']
                or self.r.headers['Content-Type'] == 'html'):
            r_type = "text"
        elif (self.r.headers['Content-Type'] == 'application/octet-stream'
                or 'application' in self.r.headers['Content-Type']):
            r_type = 'exe'
        else:
            print("Content Type detected as {}".format(self.r.headers["Content-Type"]))
            r_type = 'default'

        return r_type

    def process_file(self):
        if self.r.ok:
            req_type = self._get_content_type()

            if req_type == "text":
                if len(self.r.url.split('/')[-1]) > 0:
                    with open("../Misc_Project_Files/{}".format(self.r.url.split('/')[-1]), 'w') as f:
                        f.write(self.r.text)
                        print("{} written".format(self.r.url.split('.')[-1]))
                else:
                    with open("../Misc_Project_Files/response.html", "w") as f:
                        f.write(self.r.text)
                        print("{} written".format(f.name.split('.')[-1]))

            elif req_type == "exe":
                with open("../Misc_Project_Files/{}".format(self.r.url.split('/')[-1]), 'wb') as f:
                    f.write(self.r.content)
                    print("{} written".format(self.r.url.split('.')[-1]))
            else:
                print("request type defaulted to text since req_type was not recognized.")
                try:
                    with open("../Misc_Project_Files/{}".format(self.r.url.split('/')[-1]), 'w') as f:
                        f.write(self.r.text)
                        print("{} written".format(self.r.url.split('.')[-1]))
                except IOError as e:
                    print("error: {}".format(e))

        elif not self.r.ok:
            print("Error: {},\n{}".format(self.r.status_code, self.r.reason))
