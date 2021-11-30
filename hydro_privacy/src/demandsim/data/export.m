% =================
% Load the database
% =================
homeFolder = pwd;
addpath('.');
load database.mat

% =================
% Export signatures
% =================
mkdir('signatures');

fn = fieldnames(database.signatures);
for idx=1:numel(fn)
    values = database.signatures.(fn{idx});
    save(strcat('signatures/',fn{idx},'.mat'), 'values', '-v7');
end

% =====================
% Export UseFrequencies
% =====================
mkdir UseFrequencies;

fn = fieldnames(database.UseFrequencies);
for idx=1:numel(fn)
    mkdir(strcat('UseFrequencies/',fn{idx}));
    NumberOfEventsPerDay = database.UseFrequencies.(fn{idx}).NumberOfEventsPerDay;
    save(strcat('UseFrequencies/',fn{idx},'/NumberOfEventsPerDay.mat'), 'NumberOfEventsPerDay', '-v7');
    EventStartTime = database.UseFrequencies.(fn{idx}).EventStartTime;
    save(strcat('UseFrequencies/',fn{idx},'/EventStartTime.mat'), 'EventStartTime', '-v7');
    EventDuration = database.UseFrequencies.(fn{idx}).EventDuration;
    save(strcat('UseFrequencies/',fn{idx},'/EventDuration.mat'), 'EventDuration', '-v7');
    EventVolume = database.UseFrequencies.(fn{idx}).EventVolume;
    save(strcat('UseFrequencies/',fn{idx},'/EventVolume.mat'), 'EventVolume', '-v7');
end

% =======================
% Export UseProbabilities
% =======================
mkdir UseProbabilities;

fn = fieldnames(database.UseProbabilities);
for idx=1:numel(fn)
    mkdir(strcat('UseProbabilities/',fn{idx}));
    NumberOfEventsPerDay = database.UseProbabilities.(fn{idx}).NumberOfEventsPerDay;
    % Preallocate array of structs to maintain order of fields 
    distributions = repmat(struct('type', '', 'r', 0, 'p', 0, 'l', 0, 'n', 0), length(NumberOfEventsPerDay), 1);
    for i=1:length(NumberOfEventsPerDay)
        if isa(NumberOfEventsPerDay{i}{1}, 'prob.NegativeBinomialDistribution')
            distributions(i).type = 'NegativeBinomialDistribution';
            distributions(i).r = NumberOfEventsPerDay{i}{1}.R;
            distributions(i).p = NumberOfEventsPerDay{i}{1}.P;
        elseif isa(NumberOfEventsPerDay{i}{1}, 'prob.PoissonDistribution')
            distributions(i).type = 'PoissonDistribution';
            distributions(i).l = NumberOfEventsPerDay{i}{1}.lambda;
        elseif isa(NumberOfEventsPerDay{i}{1}, 'prob.BinomialDistribution')
            distributions(i).type = 'BinomialDistribution';
            distributions(i).n = NumberOfEventsPerDay{i}{1}.N;
            distributions(i).p = NumberOfEventsPerDay{i}{1}.p;
        end
    end
    save(strcat('UseProbabilities/',fn{idx},'/NumberOfEventsPerDay.mat'), 'distributions', '-v7');
    
    EventStartTime = database.UseProbabilities.(fn{idx}).EventStartTime;
    k.kernel = '';
    k.bandwidth = 0;
    k.support = '';
    kd = repmat(k,1,length(EventStartTime));
    for i=1:length(EventStartTime)
        kd(i).kernel = EventStartTime{i}{1}.Kernel;
        kd(i).bandwidth = EventStartTime{i}{1}.BandWidth;
        kd(i).support = EventStartTime{i}{1}.Support;
        kd(i).data = EventStartTime{i}{1}.InputData.data;
    end
    save(strcat('UseProbabilities/',fn{idx},'/EventStartTime.mat'), 'kd', '-v7');
    
    GMDurationAndVolume = database.UseProbabilities.(fn{idx}).GMDurationAndVolume;
    gmd.mu = 0;
    gmd.proportion = 0;
    gm = repmat(gmd,1,length(GMDurationAndVolume));
    for i=1:length(GMDurationAndVolume)
        gm(i).mu = GMDurationAndVolume{i}.mu;
        gm(i).proportion = GMDurationAndVolume{i}.ComponentProportion;
        gm(i).sigma = GMDurationAndVolume{i}.Sigma
    end
    save(strcat('UseProbabilities/',fn{idx},'/GMDurationAndVolume.mat'), 'gm', '-v7');
end
