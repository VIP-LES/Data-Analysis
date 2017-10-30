% Program to graph APRS data logged by aprs.fi.
% Add file to MATLAB path and run program

clear
clc

% Get unit option from user
units = input('Use Imperial Units (y/n): ', 's');

% Read data from csv file
fileName = 'aprsfi_export_KM4FFQ-11_20170408_124926_20170408_204926.csv';
fileID = fopen(fileName);
data = textscan(fileID, '%{yyyy-MM-dd HH:mm:ss}D %{yyyy-MM-dd HH:mm:ss}D %f %f %f %f %f %q', 'HeaderLines', 1, 'Delimiter', ',');

% Parse data in comments field
temp = [];
pres = [];
comment = data{1,8};
for i = 1:size(comment, 1)
    str = strsplit(comment{i});
    strTemp = str{2};
    strPres = str{3};
    temp(i) = str2double(strTemp(1:end-1));
    pres(i) = str2double(strPres(1:end-2));
end

% Unit conversions for Imperial Units
if units == 'y'
    temp = (temp * 1.8) + 32;
    data{1,7} = data{1,7} * 3.28084;
    tempLabel = 'Temperature (F)';
    altLabel = 'Altitude (ft)';
else
    tempLabel = 'Temperature (C)';
    altLabel = 'Altitude (m)';
end

% Plot temperature
subplot(3, 1, 1);
plot(data{1,1}, temp);
title('Internal Temperature');
xlabel('Time (UTC)');
ylabel(tempLabel);

% Plot pressure
subplot(3, 1, 2);
plot(data{1,1}, pres);
title('Pressure');
xlabel('Time (UTC)');
ylabel('Pressure (mb)');

% Plot Altitude
subplot(3, 1, 3);
plot(data{1,1}, data{1, 7});
title('Altitude');
xlabel('Time (UTC)');
ylabel(altLabel);