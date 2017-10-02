% Program to graph Geiger counter data logged by Verne.
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
fileName = strcat('run', int2str(runNum), '-geiger-', int2str(fileNum), '.csv');

time = [];

% While data files exist, store timestamps of radiation events
while exist(fileName, 'file')
    % Print starting time if first file
    if fileNum == 1
        startTime = csvread(fileName,0,0,[0,0,0,0]);
        fprintf('Starting time (Unix epoch): %d\n', startTime);
    end
    
    %read data
    data = csvread(fileName, 1, 0);
    % create matrix of timestamps
    time = [time, transpose(data(:,1))];
    
    fileNum = fileNum + 1;
    fileName = strcat('run', int2str(runNum), '-geiger-', int2str(fileNum), '.csv');
end

% Display an error if file not found
if fileNum == 1
    errorMessage = strcat('File "', fileName, '" not found');
    error(errorMessage);
end

% Initialize counts per minute
cpm = zeros(1, 60*(fileNum-1));

% Calculate counts per minute based on timestamps
for i = 1:size(time, 2)
    cpm(ceil(time(i)/1000/60)) = cpm(ceil(time(i)/1000/60)) + 1;
end

% Plot data
plot(1:60*(fileNum-1), cpm);
title('Geiger Counter Data');
xlabel('Time since start (min)');
ylabel('Counts per minute');