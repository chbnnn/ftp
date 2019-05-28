# -*- coding: utf-8 -*-
"""
Created on 19-5-20 下午5:28

@author: chinbing <x62881999@gmail.com>
"""

import getpass
import os
import subprocess
from ftplib import FTP, error_perm


class MyFTP:
	ftp = FTP()

	def __init__(self, host, port='21', debug_level=0):
		self.ftp.set_debuglevel(debug_level)  # 打开调试级别2，显示详细信息
		self.ftp.set_pasv(1)  # 0主动模式 1 #被动模式
		self.ftp.connect(host)

	def login(self, user, password):
		self.ftp.login(user, password)
		print(self.ftp.welcome)

	def set_debug_level(self, debug_level=0):
		self.ftp.set_debuglevel(debug_level)

	def isdir(self, remote_path):
		try:
			self.ftp.cwd(remote_path)
			self.ftp.cwd('..')
			return True
		except error_perm:
			return False

	def ls(self, long=False):
		if not long:
			nlst = self.ftp.nlst()
			for item in nlst:
				print(item, end=' ')
			print('')
		else:
			self.ftp.dir()

	def cd(self, remote_path):
		try:
			self.ftp.cwd(remote_path)
		except error_perm:
			print(' error: remote path ', remote_path, ' does not exist')

	def rm(self, remote_file):
		self.ftp.delete(remote_file)

	def rm(self, file):
		try:
			self.ftp.delete(file)
		except error_perm:
			print(' error: remote file ', file, ' does not exist')

	def mkdir(self, dir):
		self.ftp.mkd(dir)

	def rmdir(self, remote_path, rf=False):
		if not rf:
			self._rmdir(remote_path)
		else:
			self._rmdir_rf(remote_path)

	def _rmdir(self, remote_path):
		try:
			self.ftp.rmd(remote_path)
		except error_perm:
			print(' rmdir ', remote_path, ' failed: not empty')

	def _rmdir_rf(self, remote_path):
		try:
			self.ftp.cwd(remote_path)
			remote_files = self.ftp.nlst()
			for file in remote_files:
				if self.isdir(file):
					self._rmdir_rf(file)
				else:
					self.ftp.delete(file)
			self.ftp.cwd('..')
			self.ftp.rmd(remote_path)
			return True
		except error_perm:
			print(' remote directory ', remote_path, ' does not existdd')
			return False

	def download(self, remote, local_destination='./'):
		try:
			self.ftp.cwd(remote)
			self.ftp.cwd('..')
			return self._download_dir(remote, local_destination)
		except error_perm:
			return self._download(remote, local_destination)

	def _download(self, remote_file, local_destination='./'):
		if local_destination == './':
			local_destination = './' + os.path.basename(remote_file)

		with open(local_destination, 'wb') as file:
			self.ftp.retrbinary("RETR %s" % remote_file, file.write)
			return True

	def _download_dir(self, remote_dir, local_destination='./'):
		if local_destination == './':
			local_destination = os.path.basename(remote_dir)
		else:
			local_destination = local_destination

		if not os.path.isdir(local_destination):
			os.mkdir(local_destination)
			os.chdir(local_destination)

		try:
			self.ftp.cwd(remote_dir)
			remote_files = self.ftp.nlst()
			for remote_file in remote_files:
				if self.isdir(remote_file):
					self._download_dir(remote_file)
				else:
					self._download(remote_file)
			self.ftp.cwd('..')
			os.chdir('..')
			return True
		except error_perm:
			print('remote directory ', remote_dir, ' does not exist')
			return False

	def upload(self, local, remote_destination='./'):
		if not os.path.isdir(local):
			return self._upload(local, remote_destination)
		else:
			return self._upload_dir(local, remote_destination)

	def _upload(self, local_file, remote_destination='./'):
		if not os.path.isfile(local_file):
			return False
		if remote_destination == './':
			remote_destination = os.path.basename(local_file)

		with open(local_file, 'rb') as file:
			self.ftp.storbinary('STOR %s' % remote_destination, file)
			return True

	def _upload_dir(self, local_dir, remote_destination='./'):
		if not os.path.isdir(local_dir):
			return False
		if remote_destination == './':
			remote_destination = os.path.basename(local_dir)
		else:
			remote_destination = remote_destination

		try:
			self.ftp.cwd(remote_destination)
		except error_perm:
			try:
				self.ftp.mkd(remote_destination)
				self.ftp.cwd(remote_destination)
			except error_perm:
				print('You don\'t have permission for create directory')

		local_files = os.listdir(local_dir)
		for local_file in local_files:
			src = os.path.join(local_dir, local_file)
			if os.path.isdir(src):
				self._upload_dir(src)
			else:
				self._upload(src)
		self.ftp.cwd('..')
		return True

	def close(self):
		self.ftp.quit()


if __name__ == '__main__':
	host = input('host: ')
	name = input('name: ')
	password = getpass.getpass('password: ')
	ftp = MyFTP(host, debug_level=0)
	ftp.login(name, password)

	while True:
		wd = ftp.ftp.pwd()
		cmd = input('Chinbing ' + wd + '> ').split(' ')
		action = cmd[0]
		if action == 'download':
			if len(cmd) > 2:
				downloaded = ftp.download(cmd[1], cmd[2])
				if downloaded:
					print(' file(s) successfully downloaded')
			else:
				ftp.download(cmd[1])
		elif action == 'upload':
			if len(cmd) > 2:
				uploaded = ftp.upload(cmd[1], cmd[2])
				if uploaded:
					print(' file(s) successfully uploaded')
			else:
				ftp.upload(cmd[1])
		elif action == 'mkdir':
			ftp.mkdir(cmd[1])
		elif action == 'rmdir':
			if len(cmd) > 2 and cmd[1] == '-rf':
				ftp.rmdir(cmd[2], True)
			else:
				ftp.rmdir(cmd[1])
		elif action == 'cd':
			ftp.cd(cmd[1])
		elif action == 'rm':
			ftp.rm(cmd[1])
		elif action == 'ls':
			if len(cmd) > 1 and cmd[1] == '-l':
				ftp.ls(True)
			else:
				ftp.ls()
		elif action == 'debuglevel':
			ftp.set_debug_level(int(cmd[1]))
		elif action == 'exit':
			ftp.close()
			break

		elif action == 'pwd':
			subprocess.run(['pwd'])
		elif action == 'lls':
			if len(cmd) > 1 and cmd[1] == '-l':
				subprocess.run(['ls', '-l'])
			else:
				ls_result = subprocess.run(['ls'], stdout=subprocess.PIPE).stdout
				ls_result = str(ls_result, encoding='utf-8').split('\n')
				for file in ls_result:
					print(file, end=' ')
				print()
		elif action == 'lcd':
			os.chdir(cmd[1])
		else:
			print(' invalid command')

