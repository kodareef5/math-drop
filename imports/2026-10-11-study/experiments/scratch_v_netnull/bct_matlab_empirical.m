% Run the MATLAB BCT randmio_und.m (FieldTrip external/bct copy) under Octave on
% d=(4,4,2,2,2,2) and write the edge-set key of each output to a text file.
addpath('/home/claude/work/verify_repos/bct_matlab/ft');
rand('twister', 20261011);
A0 = dlmread('/home/claude/work/verify_repos/scratch_v_netnull/start_A0.txt');
runs = str2num(getenv('RUNS'));
fid = fopen('/home/claude/work/verify_repos/scratch_v_netnull/bct_matlab_keys.txt', 'w');
for r = 1:runs
  R = randmio_und(A0, 10);
  [i, j] = find(triu(R));
  fprintf(fid, '%s\n', sprintf('%d%d,', [i'-1; j'-1]));
end
fclose(fid);
