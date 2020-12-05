clear
close all
fid = fopen('dwt.bin','r'); im4 = fread(fid, [64,64], 'int32'); fclose(fid);
figure;
imagesc(im4);
