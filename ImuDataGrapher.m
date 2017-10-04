% Program to graph IMU data logged by Verne.
% Add files using default names to MATLAB path and run
% program. Input the appropriate run number for the
% desired graph.

clear
clc

% Get run number input from user
runNum = input('Run number: ');

% Get axis display settings from user
accelOpt = input('Acceleration axes to display (some combination of xyz): ', 's');

% Vector of axes options x, y, z
accelAxes = [1, 1, 1];

% Set axes based on input
if ~isempty(accelOpt)
    x = contains(accelOpt, 'x', 'IgnoreCase', true);
    y = contains(accelOpt, 'y', 'IgnoreCase', true);
    z = contains(accelOpt, 'z', 'IgnoreCase', true);
    accelAxes = [x, y, z];
end

% Get axis display settings from user
rotOpt = input('Rotation axes to display (some combination of xyz): ', 's');

% Vector of axes options x, y, z
rotAxes = [1, 1, 1];

% Set axes based on input
if ~isempty(rotOpt)
    x = contains(rotOpt, 'x', 'IgnoreCase', true);
    y = contains(rotOpt, 'y', 'IgnoreCase', true);
    z = contains(rotOpt, 'z', 'IgnoreCase', true);
    rotAxes = [x, y, z];
end

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
accelLeg = {};
if accelAxes(1)
    plot(time, accelX, 'Color', [0, 0.447, 0.7410]);
    accelLeg = [accelLeg, cellstr('x')];
    hold on
end
if accelAxes(2)
    plot(time, accelY, 'Color', [0.85, 0.325, 0.098]);
    accelLeg = [accelLeg, cellstr('y')];
    hold on
end
if accelAxes(3)
    plot(time, accelZ, 'Color', [0.929, 0.694, 0.125]);
    accelLeg = [accelLeg, cellstr('z')];
    hold on
end
hold off
title('Acceleration Data');
xlabel('Time since start (ms)');
ylabel('Acceleration (m/s^2)');
legend(accelLeg);

% Plot rotation data
subplot(2, 1, 2);
rotLeg = {};
if rotAxes(1)
    plot(time, rotX, 'Color', [0, 0.447, 0.7410]);
    rotLeg = [rotLeg, cellstr('x')];
    hold on
end
if rotAxes(2)
    plot(time, rotY, 'Color', [0.85, 0.325, 0.098]);
    rotLeg = [rotLeg, cellstr('y')];
    hold on
end
if rotAxes(3)
    plot(time, rotZ, 'Color', [0.929, 0.694, 0.125]);
    rotLeg = [rotLeg, cellstr('z')];
    hold on
end
hold off
title('Rotation Data');
xlabel('Time since start (ms)');
ylabel('Rotation (deg)');
legend(rotLeg);