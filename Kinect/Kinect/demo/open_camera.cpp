// Kinect.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <cstdio>
#include <k4a/k4a.h>
#include <k4arecord/record.h>
#include <k4arecord/playback.h>

using namespace std;

int openCamera()
{
	uint32_t count = k4a_device_get_installed_count();
	if (count == 0)
	{
		printf("No k4a devices attached!\n");
		return 1;
	}

	// Open the first plugged in Kinect device
	k4a_device_t device = NULL;
	if (K4A_FAILED(k4a_device_open(K4A_DEVICE_DEFAULT, &device)))
	{
		printf("Failed to open k4a device!\n");
		return 1;
	}

	// Get the size of the serial number
	size_t serial_size = 0;
	k4a_device_get_serialnum(device, NULL, &serial_size);

	// Allocate memory for the serial, then acquire it
	char* serial = (char*)(malloc(serial_size));
	k4a_device_get_serialnum(device, serial, &serial_size);
	printf("Opened device: %s\n", serial);
	free(serial);

	// Configure a stream of 4096x3072 BRGA color data at 15 frames per second
	k4a_device_configuration_t config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
	config.camera_fps = K4A_FRAMES_PER_SECOND_15;
	config.color_format = K4A_IMAGE_FORMAT_COLOR_BGRA32;
	config.color_resolution = K4A_COLOR_RESOLUTION_3072P;

	// Start the camera with the given configuration
	if (K4A_FAILED(k4a_device_start_cameras(device, &config)))
	{
		printf("Failed to start cameras!\n");
		k4a_device_close(device);
		return 1;
	}

	// Camera capture and application specific code would go here

	// Shut down the camera when finished with application logic
	k4a_device_stop_cameras(device);
	k4a_device_close(device);

	return 0;
}

// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
