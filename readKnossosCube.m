

% READKNOSSOSCUBE: Read raw data from EM into Matlab
%
%   The function has the following arguments:
%       KL_PARFOLDER: Give the root directory of the data you want to read as a
%           string, e.g. 'E:\e_k0563\k0563_mag1\'
%       KL_FILEPREFIX: Give the name of the specific file you want to read without
%           the coordinates or the ending as a string, e.g. '100527_k0563_mag1'
%       KL_CUBECOORD: Give an array of 3 numbers of the xyz-coordinates as
%           given in the file name, no need for the full four digits: 0020 ->
%           20. E.g. [21 30 150]
%       CLASST: Optional! Standard version is unsigned int with 8 bits. For the
%           precision of the values.
%       cubesize: size of a knossos-cube (Default [128, 128, 128, 1])-
%       returnZeros: (Optional) Logical flag indicating that zeros should
%           be returned if cube does not exist. Otherwise [] is returned.
%           (Default: true)
%
%   Moritz Helmstaedter
%   moritz.helmstaedter@brain.mpg.de
%   Max Planck Gesellschaft
%
%   => readKnossosCube( �E:\e_k0563\k_0563_mag1', �100527_k0563_mag1�, [21 30 150], �uint8� )
%

% Building the full filename
kl_fullfile = '/home/mdm/Pictures/knossTest/knossos_cuber_project_mag1_x0044_y0030_z0006.raw';


  %kl_parfolder, sprintf( 'x%04.0f', kl_cubeCoord(1) ),...
  %  sprintf( 'y%04.0f', kl_cubeCoord(2) ), sprintf( 'z%04.0f', kl_cubeCoord(3) ),...
  %  sprintf( ['%s_x%04.0f_y%04.0f_z%04.0f%s.' ending], kl_fileprefix, kl_cubeCoord, kl_filesuffix ) );

classT = 'uint8=>uint8';
fid = fopen( kl_fullfile );
kl_cube = fread(fid, classT);
fclose(fid);
disp('ok')
