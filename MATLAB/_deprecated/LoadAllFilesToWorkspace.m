%%% put this in a new script, in a function it WILL NOT WORK!
%%% and fix your paths, ofc. i left mine in here on purpose.



%%% SETTINGS
%folderName='/home/ktr/Documents/MATLAB/Mininet/itg-logs/';
folderName='/cygdrive/c/Users/sjas/work/ktr/MATLAB/itg-logs/';
extension='*.dat';


%%% CODE
concattedString=strcat(folderName, extension);
fileSet=dir(concattedString); 
% loop from 1 through to the amount of rows
for i = 1:length(fileSet)
    % load file with absolute path, 
    %the fileSet provides just the single filename
    load (strcat(folderName, fileSet(i).name)); 
end

%%% TIDY UP so only imported files stay in workspace area
clear folderName;
clear extension;
clear concattedString;
clear fileSet;
clear i;
