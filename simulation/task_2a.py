
import time

import numpy as np
import cv2
import os, sys
import traceback
##############################################################


try:
	import sim

except Exception:
	print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
	print('\n[WARNING] Make sure to have following files in the directory:')
	print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')
	sys.exit()


client_id = -1


def init_remote_api_server():

	global client_id

	##############	ADD YOUR CODE HERE	##############

	sim.simxFinish(-1)  # just in case, close all opened connections
	client_id = sim.simxStart("127.0.0.1", 19997, True, True, 5000, 5)  # start aconnection


	##################################################

	return client_id


def start_simulation():


	global client_id

	return_code = 0


	return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_blocking)
	time.sleep(0.5)
	return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)




	return return_code


def get_vision_sensor_image():


	global client_id

	vision_sensor_image = []
	image_resolution = []
	return_code = 0

	##############	ADD YOUR CODE HERE	##############

	# Get the handle of vision sensor
	code, visionSensorHandle = sim.simxGetObjectHandle(client_id, 'vision_sensor_1', sim.simx_opmode_blocking)

	# Get the image of vision sensor
	return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, visionSensorHandle, 0, sim.simx_opmode_streaming)

	time.sleep(2)
	return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, visionSensorHandle, 0,  sim.simx_opmode_buffer)

	##################################################

	return vision_sensor_image, image_resolution, return_code


def transform_vision_sensor_image(vision_sensor_image, image_resolution):

	transformed_image = None

	##############	ADD YOUR CODE HERE	##############

	transformed_image = np.array(vision_sensor_image, dtype=np.uint8)
	transformed_image.resize([image_resolution[0], image_resolution[1], 3])

	transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB)
	transformed_image = cv2.flip(transformed_image, 0)

	##################################################

	return transformed_image


def stop_simulation():


	global client_id

	return_code = 0

	##############	ADD YOUR CODE HERE	##############

	return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot)


	##################################################

	return return_code


def exit_remote_api_server():

	global client_id

	##############	ADD YOUR CODE HERE	##############

	sim.simxFinish(-1)


if __name__ == "__main__":

	# Import 'task_1b.py' file as module
	try:
		import task_1b

	except ImportError:
		print('\n[ERROR] task_1b.py file is not present in the current directory.')
		print('Your current directory is: ', os.getcwd())
		print('Make sure task_1b.py is present in this current directory.\n')
		sys.exit()

	except Exception as e:
		print('Your task_1b.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()


	# Import 'task_1a_part1.py' file as module
	try:
		import task_1a_part1

	except ImportError:
		print('\n[ERROR] task_1a_part1.py file is not present in the current directory.')
		print('Your current directory is: ', os.getcwd())
		print('Make sure task_1a_part1.py is present in this current directory.\n')
		sys.exit()

	except Exception as e:
		print('Your task_1a_part1.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	# Initiate the Remote API connection with CoppeliaSim server
	print('\nConnection to CoppeliaSim Remote API Server initiated.')
	print('Trying to connect to Remote API Server...')

	try:
		client_id = init_remote_api_server()

		if (client_id != -1):
			print('\nConnected successfully to Remote API Server in CoppeliaSim!')

			# Starting the Simulation
			try:
				return_code = start_simulation()

				if (return_code == sim.simx_return_novalue_flag):
					print('\nSimulation started correctly in CoppeliaSim.')

				else:
					print('\n[ERROR] Failed starting the simulation in CoppeliaSim!')
					print('start_simulation function is not configured correctly, check the code!')
					print()
					sys.exit()

			except Exception:
				print('\n[ERROR] Your start_simulation function throwed an Exception, kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()

		else:
			print('\n[ERROR] Failed connecting to Remote API server!')
			print('[WARNING] Make sure the CoppeliaSim software is running and')
			print('[WARNING] Make sure the Port number for Remote API Server is set to 19997.')
			print('[ERROR] OR init_remote_api_server function is not configured correctly, check the code!')
			print()
			sys.exit()

	except Exception:
		print('\n[ERROR] Your init_remote_api_server function throwed an Exception, kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually if started.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		sys.exit()

	# Get image array and its resolution from Vision Sensor in ComppeliaSim scene
	try:
		vision_sensor_image, image_resolution, return_code = get_vision_sensor_image()

		if ((return_code == sim.simx_return_ok) and (len(image_resolution) == 2) and (len(vision_sensor_image) > 0)):
			print('\nImage captured from Vision Sensor in CoppeliaSim successfully!')

			# Get the transformed vision sensor image captured in correct format
			try:
				transformed_image = transform_vision_sensor_image(vision_sensor_image, image_resolution)

				if (type(transformed_image) is np.ndarray):

					cv2.imshow('transformed image', transformed_image)
					cv2.waitKey(0)
					cv2.destroyAllWindows()

					# Get the resultant warped transformed vision sensor image after applying Perspective Transform
					try:
						warped_img = task_1b.applyPerspectiveTransform(transformed_image)

						if (type(warped_img) is np.ndarray):

							# Get the 'shapes' dictionary by passing the 'warped_img' to scan_image function
							try:
								shapes = task_1a_part1.scan_image(warped_img)

								if (type(shapes) is dict):
									print('\nShapes detected by Vision Sensor are: ')
									print(shapes)

									inp_char = input('\nEnter \'q\' or \'Q\' to quit the program: ')

									if (len(inp_char) == 1) and ((inp_char == 'q') or (inp_char == 'Q')):
										print('\nQuitting the program and stopping the simulation by calling stop_simulation and exit_remote_api_server functions.')

										# Ending the Simulation
										try:
											return_code = stop_simulation()

											if (return_code == sim.simx_return_novalue_flag):
												print('\nSimulation stopped correctly.')

												# Stop the Remote API connection with CoppeliaSim server
												try:
													exit_remote_api_server()

													if (start_simulation() == sim.simx_return_initialize_error_flag):
														print('\nDisconnected successfully from Remote API Server in CoppeliaSim!')

													else:
														print('\n[ERROR] Failed disconnecting from Remote API server!')
														print('[ERROR] exit_remote_api_server function is not configured correctly, check the code!')

												except Exception:
													print('\n[ERROR] Your exit_remote_api_server function throwed an Exception, kindly debug your code!')
													print('Stop the CoppeliaSim simulation manually.\n')
													traceback.print_exc(file=sys.stdout)
													print()
													sys.exit()

											else:
												print('\n[ERROR] Failed stopping the simulation in CoppeliaSim server!')
												print('[ERROR] stop_simulation function is not configured correctly, check the code!')
												print('Stop the CoppeliaSim simulation manually.')

											print()
											sys.exit()

										except Exception:
											print('\n[ERROR] Your stop_simulation function throwed an Exception, kindly debug your code!')
											print('Stop the CoppeliaSim simulation manually.\n')
											traceback.print_exc(file=sys.stdout)
											print()
											sys.exit()

									else:
										print('\n[WARNING] Kindly provide input of "q" or "Q" only!')
										print('Stop the CoppeliaSim simulation manually.')
										print()
										sys.exit()

								else:
									print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.')
									print('Stop the CoppeliaSim simulation manually.')
									print()
									sys.exit()

							except Exception:
								print('\n[ERROR] Your scan_image function in task_1a_part1.py throwed an Exception, kindly debug your code!')
								print('Stop the CoppeliaSim simulation manually.\n')
								traceback.print_exc(file=sys.stdout)
								print()
								sys.exit()

						else:
							print('\n[ERROR] applyPerspectiveTransform function is not configured correctly, check the code.')
							print('Stop the CoppeliaSim simulation manually.')
							print()
							sys.exit()

					except Exception:
						print('\n[ERROR] Your applyPerspectiveTransform function in task_1b.py throwed an Exception, kindly debug your code!')
						print('Stop the CoppeliaSim simulation manually.\n')
						traceback.print_exc(file=sys.stdout)
						print()
						sys.exit()

				else:
					print('\n[ERROR] transform_vision_sensor_image function is not configured correctly, check the code.')
					print('Stop the CoppeliaSim simulation manually.')
					print()
					sys.exit()

			except Exception:
				print('\n[ERROR] Your transform_vision_sensor_image function throwed an Exception, kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()

		else:
			print('\n[ERROR] get_vision_sensor function is not configured correctly, check the code.')
			print('Stop the CoppeliaSim simulation manually.')
			print()
			sys.exit()

	except Exception:
		print('\n[ERROR] Your get_vision_sensor_image function throwed an Exception, kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		sys.exit()

