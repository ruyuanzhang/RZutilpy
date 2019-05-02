function [profile,mv_length] = envelope(time_sigma,frame_rate,cut_off,amplitude)
%%%
time_sigma = time_sigma*1000;
if cut_off
    gauss_only = 0;
else
    gauss_only = 1;
end
k = 1;
fr = round(frame_rate/20);
xx = 1:fr;
for time1 = 7:0.25:25
    x1(k) = time1;
    time = time1/(1000/frame_rate);
    time_gauss = exp(-((xx)/(sqrt(2)*time)).^2);
    cum1(k) = sum(time_gauss)*2;
    k = k + 1;
end
[p S] = polyfit(cum1,x1,2);
area = time_sigma*frame_rate/400;
if cut_off > -1
    uniform = floor(area - 3);
    if (time_sigma > cut_off) & (~gauss_only)
        remd = area - uniform;
        time = p(1)*remd^2 + p(2)*remd + p(3);
        time = time/(1000/frame_rate);
        clear xx;
        xx = 1:fr;
        time_gauss = exp(-((xx)/(sqrt(2)*time)).^2);
        profile = ones(1,uniform + 2*fr);
        profile(1:fr) = fliplr(time_gauss);
        profile(uniform + 2*fr - (fr - 1):uniform + 2*fr) = time_gauss;
    else
        time = time_sigma/(1000/frame_rate);
        mv_length = time*(1000/frame_rate)*6;
        mv_length = round(((round(mv_length/(1000/frame_rate)))/2))*2 + 1;
        xx = 1:mv_length;
        xx = (xx - mean(xx));
        profile = exp(-((xx)/(sqrt(2)*time)).^2);
    end
    small = sum(amplitude*profile < .5)/2;
    profile = profile(small + 1:size(profile,2) - small);
    mv_length = size(profile,2);
else
    mv_length = round(area);
    profile = ones(1,mv_length);
end
profile = profile*amplitude;