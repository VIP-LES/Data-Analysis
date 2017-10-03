% Program to graph IMU data logged by Verne.
% Add files using default names to MATLAB path and run
% program. Input the appropriate run number for the
% desired graph.

clear
clc

% Get run number input from user
runNum = input('Run number: ');

% Beginning file number is 1
fileNum = 1;

% Format file name as run#-geiger-#.csv
fileName = strcat('run', int2str(runNum), '-imu-', int2str(fileNum), '.csv');

data = [];

% While data files exist, store timestamps of radiation events
while exist(fileName, 'file')
    % Print starting time if first file
    if fileNum == 1
        startTime = csvread(fileName,0,0,[0,0,0,0]);
        fprintf('Starting time (Unix epoch): %d\n', startTime);
    end
    
    %read data
    data = [data; csvread(fileName, 1, 0)];
    
    fileNum = fileNum + 1;
    fileName = strcat('run', int2str(runNum), '-imu-', int2str(fileNum), '.csv');
end

% Display an error if file not found
if fileNum == 1
    errorMessage = strcat('File "', fileName, '" not found');
    error(errorMessage);
end

time = data(:,1);

accelX = data(:,2);
accelY = data(:,3);
accelZ = data(:,4);

rotX = data(:,5);
rotY = data(:,6);
rotZ = data(:,7);

% Plot acceleration data
subplot(2, 1, 1);
plot(time, accelX, time, accelY, time, accelZ);
title('Acceleration Data');
xlabel('Time since start (ms)');
ylabel('Acceleration (m/s^2)');
legend('x', 'y', 'z');

% Plot rotation data
subplot(2, 1, 2);
plot(time, rotX, time, rotY, time, rotZ);
title('Rotation Data');
xlabel('Time since start (ms)');
ylabel('Rotation (deg)');
legend('x', 'y', 'z');