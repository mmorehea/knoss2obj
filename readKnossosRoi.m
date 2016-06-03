function kl_roi = readKnossosRoi( kl_parfolder, kl_fileprefix, kl_bbox, classT, kl_filesuffix, ending, numChannels)
% READKNOSSOSROI: Read multiple raw data from EM into Matlab selecting a
%       region of interest
%
%   The function has the following arguments:
%       KL_PARFOLDER: Give the root directory of the data you want to read as a
%           string, e.g. 'E:\e_k0563\k0563_mag1\'
%       KL_FILEPREFIX: Give the name of the specific files you want to read without
%           the coordinates or the ending as a string, e.g. '100527_k0563_mag1'
%       KL_BBOX: Give an 3x2 array of the pixel coordinates of your region of
%           interest, no need for the full four digits: 0020 -> 20.
%           E.g. [129 384; 129 384; 129 384] CAREFUL: The amount of data will
%           easily explode.
%       CLASST: Optional! Standard version is unsigned int with 8 bits. For the
%           precision of the values.
%       NumChannels: (Optional) Number of channels per voxel.
%           (Default: 1)
%
%   Moritz Helmstaedter
%   moritz.helmstaedter@brain.mpg.de
%   Max Planck Gesellschaft
%
%   => readKnossosRoi( 'E:\e_k0563\k0563_mag1', '100527_k0563_mag1',
%           [129 384; 129 384; 129 384], 'uint8' )

    if ~exist('classT','var') || isempty(classT)
        classT = 'uint8';
    end
    if ~exist('ending','var') || isempty(ending)
        ending = 'raw';
    end
    if ~exist('kl_filesuffix','var') || isempty(kl_filesuffix)
        kl_filesuffix = '';
    end
    if ~exist('numChannels','var') || isempty(numChannels)
        numChannels = 1;
    end
    cubesize = [128, 128, 128, numChannels];

   % Calculate the size of the roi in pixels and xyz-coordinates
    kl_bbox_size = kl_bbox(:,2)' - kl_bbox(:,1)' + [1 1 1];
    kl_bbox_cubeind = [floor(( kl_bbox(:,1) - 1) / 128 ) ceil( kl_bbox(:,2) / 128 ) - 1];

    kl_roi = zeros( [kl_bbox_size, numChannels], classT );

    % Read every cube touched with readKnossosCube and write it in the right
    % place of the kl_roi matrix
    for kl_cx = kl_bbox_cubeind(1,1) : kl_bbox_cubeind(1,2)
        for kl_cy = kl_bbox_cubeind(2,1) : kl_bbox_cubeind(2,2)
            for kl_cz = kl_bbox_cubeind(3,1) : kl_bbox_cubeind(3,2)

                kl_thiscube_coords = [[kl_cx, kl_cy, kl_cz]', [kl_cx, kl_cy, kl_cz]' + 1] * 128;
                kl_thiscube_coords(:,1) = kl_thiscube_coords(:,1) + 1;

                kl_validbbox = [max( kl_thiscube_coords(:,1), kl_bbox(:,1) ),...
                    min( kl_thiscube_coords(:,2), kl_bbox(:,2) )];

                kl_validbbox_cube = kl_validbbox - repmat( kl_thiscube_coords(:,1), [1 2] ) + 1;
                kl_validbbox_roi = kl_validbbox - repmat( kl_bbox(:,1), [1 2] ) + 1;

                kl_cube = readKnossosCube( kl_parfolder, kl_fileprefix, ...
                    [kl_cx, kl_cy, kl_cz], [classT '=>' classT], ...
                    kl_filesuffix, ending, cubesize );

                kl_roi( kl_validbbox_roi(1,1) : kl_validbbox_roi(1,2),...
                    kl_validbbox_roi(2,1) : kl_validbbox_roi(2,2),...
                    kl_validbbox_roi(3,1) : kl_validbbox_roi(3,2), : ) = ...
                    kl_cube( kl_validbbox_cube(1,1) : kl_validbbox_cube(1,2),...
                    kl_validbbox_cube(2,1) : kl_validbbox_cube(2,2),...
                    kl_validbbox_cube(3,1) : kl_validbbox_cube(3,2), : );
                
            end
        end
    end
    
    [x, y, z] = meshgrid(kl_bbox(2,1):kl_bbox(2,2), kl_bbox(1,1):kl_bbox(1,2),...
                        kl_bbox(3,1):kl_bbox(3,2));
    x = single(x);
    y = single(y);
    z = single(z);
    kl_roi = single(kl_roi);
    [F, V] = MarchingCubes(x, y, z, kl_roi, 0);
    
    output_name = strcat('obj\', kl_fileprefix, '.obj');
    file = fopen(output_name, 'w');
    for i = 1:length(V)
        fprintf(file, 'v %0.3f %0.3f %0.3f \n', V(i,1), V(i,2), V(i,3));
    end
    for i = 1:length(F)
        fprintf(file, 'f %0.3f %0.3f %0.3f \n', F(i,1), F(i,2), F(i,3));
    end
    
    fclose(file);