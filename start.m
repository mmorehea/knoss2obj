path = [pwd,'/',mfilename];
path = path(1:length(path)-6);
addpath(genpath(path));

cd data
file_names = dir;
cd ..

prefix_pattern = '([a-zA-z_0-9]+mag1)_x[0-9]+_y[0-9]+_z[0-9]+.raw';
x_pattern = '[a-zA-z_0-9]+mag1_x([0-9]+)_y[0-9]+_z[0-9]+.raw';
y_pattern = '[a-zA-z_0-9]+mag1_x[0-9]+_y([0-9]+)_z[0-9]+.raw';
z_pattern = '[a-zA-z_0-9]+mag1_x[0-9]+_y[0-9]+_z([0-9]+).raw';

x = zeros(numel(file_names)-2,1);
y = zeros(numel(file_names)-2,1);
z = zeros(numel(file_names)-2,1);

s = regexp(file_names(i).name, prefix_pattern, 'tokens');
prefix = s{1}{1};

for i=3:numel(file_names)
    s = regexp(file_names(i).name, x_pattern, 'tokens');
    x(i-2,1) = str2num(s{1}{1});
    s = regexp(file_names(i).name, y_pattern, 'tokens');
    y(i-2,1) = str2num(s{1}{1});
    s = regexp(file_names(i).name, z_pattern, 'tokens');
    z(i-2,1) = str2num(s{1}{1});
end

min_x = min(x) * 128;
max_x = (max(x) * 128) + 128;
min_y = min(y) * 128;
max_y = (max(y) * 128) + 128;
min_z = min(z) * 128;
max_z = (max(z) * 128) + 128;

readKnossosRoi( 'J:\code\knoss2obj\data', prefix, [min_x max_x; min_y max_y; min_z max_z], 'uint16' )