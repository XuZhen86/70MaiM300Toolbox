from absl import flags

from m300_toolbox.actions import (
    action, formatsdcard, generatetoken, getfilecounts, getfileentries, getfiles, getparkingwire,
    getsdcardstatus, getsettings, reset, sendcommandwithparams, setaudiorecording, setautoofftime,
    setchimeonboot, setdateformat, seteventsensitivity, setflickerfrequency, setlanguage,
    setrecording, settimelapserecording, settimestamp, setvideocodec, setvideoresolution,
    setvideosplittime, setvoicecontrol, setvolume, setwifionboot, setwifipassword)

ACTIONS: set[action.Action] = {
    formatsdcard.FormatSdCard(),
    generatetoken.GenerateToken(),
    getfilecounts.GetFileCounts(),
    getfileentries.GetFileEntries(),
    getfiles.GetFiles(),
    getparkingwire.GetParkingWire(),
    getsdcardstatus.GetSdCardStatus(),
    getsettings.GetSettings(),
    reset.Reset(),
    sendcommandwithparams.SendCommandWithParams(),
    setaudiorecording.SetAudioRecording(),
    setautoofftime.SetAutoOffTime(),
    setchimeonboot.SetChimeOnBoot(),
    setdateformat.SetDateFormat(),
    seteventsensitivity.SetEventSensitivity(),
    setflickerfrequency.SetFlickerFrequency(),
    setlanguage.SetLanguage(),
    setrecording.SetRecording(),
    settimelapserecording.SetTimeLapseRecording(),
    settimestamp.SetTimestamp(),
    setvideocodec.SetVideoCodec(),
    setvideoresolution.SetVideoResolution(),
    setvideosplittime.SetVideoSplitTime(),
    setvideosplittime.SetVideoSplitTime(),
    setvoicecontrol.SetVoiceControl(),
    setvolume.SetVolume(),
    setwifionboot.SetWifiOnBoot(),
    setwifipassword.SetWifiPassword(),
}

for action in ACTIONS:
  flags.register_validator(action.FLAG, action.flag_validator)
