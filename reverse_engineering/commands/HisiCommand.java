package com.banyac.dashcam.constants;

import android.content.Context;
import android.text.TextUtils;
import c.m0;
import com.banyac.dashcam.DashCam;
import com.banyac.dashcam.model.hisi.HisiFileNode;
import com.banyac.dashcam.ui.activity.BaseDeviceActivity;
import com.banyac.dashcam.ui.activity.MainActivity;
import com.banyac.key.BanyacKeyUtils;
import com.banyac.midrive.base.utils.r;
import io.reactivex.b0;
import java.text.SimpleDateFormat;
import java.util.Calendar;
/* compiled from: HisiCommand.java */
/* loaded from: /tmp/jadx-16739929987241663617.dex */
public class c {
    public static final String A = "setaudiooutvolume.cgi";
    public static final String A0 = "setdateformat.cgi";
    public static final String A1 = "enablewifi";
    private static final String A2 = "tpms_id_rf";
    public static final String B = "getcapability.cgi";
    public static final String B0 = "setgpstime.cgi";
    public static final String B1 = "wifikey";
    private static final String B2 = "tpms_id_lr";
    public static final String C = "getparameter.cgi";
    public static final String C0 = "setwakeupvideo.cgi";
    public static final String C1 = "time";
    private static final String C2 = "tpms_id_rr";
    public static final String D = "setparameter.cgi";
    public static final String D0 = "getwakeupvideo.cgi";
    public static final String D1 = "workmode";
    private static final String D2 = "direction";
    public static final String E = "setparkingattr.cgi";
    public static final String E0 = "stopparkingrec.cgi";
    public static final String E1 = "value";
    private static final String E2 = "longpress";
    public static final String F = "getparkingattr.cgi";
    public static final String F0 = "getdvrstate.cgi";
    public static final String F1 = "videoencode";
    private static final String F2 = "motor_position_normal";
    public static final String G = "setlapserecattr.cgi";
    public static final String G0 = "getdatacollectauth.cgi";
    public static final String G1 = "entertime";
    private static final String G2 = "motor_position_parking";
    public static final String H = "getsdstate.cgi";
    public static final String H0 = "getsatelitestatus.cgi";
    public static final String H1 = "threshold";
    private static final String H2 = "status";
    public static final String I = "sdcommand.cgi";
    public static final String I0 = "setnetworksynctime.cgi";
    public static final String I1 = "delaytime";
    public static final String I2 = "animate";
    public static final String J = "client.cgi";
    public static final String J0 = "setrestrictionboard.cgi";
    public static final String J1 = "format";
    public static final String J2 = "enable_boot";
    public static final String K = "setaccessalbum.cgi";
    public static final String K0 = "setblemode.cgi";
    public static final String K1 = "level";
    public static final String K2 = "boot_prompt_text";
    public static final String L = "setota.cgi";
    public static final String L0 = "setdatacollectauth.cgi";
    public static final String L1 = "operation";
    public static final String L2 = "enable_shutdown";
    public static final String M = "setwifiboot.cgi";
    public static final String M0 = "getstreamlicensed.cgi";
    public static final String M1 = "ip";
    public static final String M2 = "shutdown_prompt_text";
    public static final String N = "setlapserecattr.cgi";
    public static final String N0 = "setwifistream.cgi";
    public static final String N1 = "enable";
    public static final String N2 = "brithday_month";
    public static final String O = "reset.cgi";
    public static final String O0 = "SecretKeyConfirm.cgi";
    public static final String O1 = "devtype";
    public static final String O2 = "brithday_day";
    public static final String P = "setadasattr.cgi";
    public static final String P0 = "settpmsbind.cgi";
    public static final String P1 = "softver";
    public static final String P2 = "emergency_video_sens";
    public static final String Q = "getadasattr.cgi";
    public static final String Q0 = "gettpmstempthres.cgi";
    public static final String Q1 = "count";
    public static final String Q2 = "emergency_video_enable";
    public static final String R = "setedogattr.cgi";
    public static final String R0 = "settpmstempthres.cgi";
    public static final String R1 = "md5";
    public static final String R2 = "collision_detection_enable";
    public static final String S = "getedogattr.cgi";
    public static final String S0 = "settpmspressthres.cgi";
    public static final String S1 = "adas_on";
    public static final String S2 = "collision_detection_sens";
    public static final String T = "getparkingwire.cgi";
    public static final String T0 = "gettpmspressthres.cgi";
    public static final String T1 = "adas_environment_lable";
    public static final String T2 = "collision_response_strategy";
    public static final String U = "getgpsstatus.cgi";
    public static final String U0 = "gettpmsinfo.cgi";
    public static final String U1 = "adas_limber_launch";
    public static final String U2 = "nomove_autoshutdown_time";
    public static final String V = "setvoicecontrol.cgi";
    public static final String V0 = "settpmsunbind.cgi";
    public static final String V1 = "adas_lane_departure";
    public static final String V2 = "volum_mute_enable";
    public static final String W = "setp1n0.cgi";
    public static final String W0 = "getmotorcalibration.cgi";
    public static final String W1 = "adas_limber_crash";
    public static final String W2 = "volume_level";
    public static final String X = "setbacksensorrec.cgi";
    public static final String X0 = "setmotorposition.cgi";
    public static final String X1 = "adas_people_crash";
    public static final String X2 = "parking_activity_enable";
    public static final String Y = "getbacksensor.cgi";
    public static final String Y0 = "setmotorangle.cgi";
    public static final String Y1 = "adas_nonmotor_vehicle";
    public static final String Y2 = "parking_activity_sens";
    public static final String Z = "setrearview.cgi";
    public static final String Z0 = "getmotorangle.cgi";
    public static final String Z1 = "edog_on";
    public static final String Z2 = "parking_light_enable";
    private static final String a = "c";
    public static final String a0 = "quitguidemode.cgi";
    public static final String a1 = "getdvrlog.cgi";
    public static final String a2 = "edog_photo_enable";
    public static final String a3 = "voltage_threshold";
    public static String b = null;
    public static final String b0 = "setguidemode.cgi";
    public static final String b1 = "setuserinfo.cgi";
    public static final String b2 = "edog_ratelimit_enable";
    public static final String b3 = "sensor";
    public static int c = 0;
    public static final String c0 = "setsplittime.cgi";
    public static final String c1 = "setscreenofftype.cgi";
    public static final String c2 = "edog_roadconditions_enable";
    public static final String d = "Front";
    public static final String d0 = "setwdr.cgi";
    public static final String d1 = "setvoiceprompt.cgi";
    public static final String d2 = "ntscpal";
    public static final String e = "Back";
    public static final String e0 = "fatiguedriving.cgi";
    public static final String e1 = "setadascalib.cgi";
    public static final String e2 = "language";
    public static final String f = "F.MP4";
    public static final String f0 = "setlanguage.cgi";
    public static final String f1 = "get4gstatus.cgi";
    public static final String f2 = "timezone";
    public static final String g = "B.MP4";
    public static final String g0 = "setlcdbrightness.cgi";
    public static final String g1 = "setsoundenable.cgi";
    public static final String g2 = "zonetype";
    public static final String h = "getdeviceattr.cgi";
    public static final String h0 = "setscreensaver.cgi";
    public static final String h1 = "setparkingenable.cgi";
    public static final String h2 = "packver";
    public static final String i = "record.cgi";
    public static final String i0 = "setlogoosd.cgi";
    public static final String i1 = "setparkingsens.cgi";
    public static final String i2 = "pktlen";
    public static final String j = "setsystime.cgi";
    public static final String j0 = "getparkingattr.cgi";
    public static final String j1 = "setemergencyenable.cgi";
    public static final String j2 = "splittime";
    public static final String k = "getsystime.cgi";
    public static final String k0 = "setvoltagethreshold.cgi";
    public static final String k1 = "setspeakermute.cgi";
    public static final String k2 = "usr";
    public static final String l = "photo.cgi";
    public static final String l0 = "setimagingstyle.cgi";
    public static final String l1 = "setspeakervolume.cgi";
    public static final String l2 = "stop";
    public static final String m = "getfilecount.cgi";
    public static final String m0 = "setautosync.cgi";
    public static final String m1 = "setparkingactivityenable.cgi";
    public static final String m2 = "speedUnit";
    public static final String n = "getfilelist.cgi";
    public static final String n0 = "BindByBanya.cgi";
    public static final String n1 = "setparkingactivitysens.cgi";
    public static final String n2 = "type";
    public static final String o = "getgpsfilelist.cgi";
    public static final String o0 = "UserconfirmByBanya.cgi";
    public static final String o1 = "setparkinglightenable.cgi";
    public static final String o2 = "filepath";
    public static final String p = "getgpsstoragedata.cgi";
    public static final String p0 = "settimezone.cgi";
    public static final String p1 = "setkeyvolume.cgi";
    public static final String p2 = "source";
    public static final String q = "delete.cgi";
    public static final String q0 = "gettimezone.cgi";
    public static final String q1 = "seteffectimmediately.cgi";
    public static final String q2 = "secretbody";
    public static final String r = "getAllMenu.cgi";
    public static final String r0 = "getgpswartermarkctrl.cgi";
    public static final String r1 = "timestamp";
    private static final String r2 = "press_f";
    public static final String s = "getwifi.cgi";
    public static final String s0 = "setgpswatermarkctrl.cgi";
    public static final String s1 = "signkey";
    private static final String s2 = "press_r";
    public static final String t = "setwifi.cgi";
    public static final String t0 = "getusbsupplystate.cgi";
    public static final String t1 = "cmd";
    private static final String t2 = "temp_f";
    public static final String u = "setbootmusic.cgi";
    public static final String u0 = "getEdogVersion.cgi";
    public static final String u1 = "time";
    private static final String u2 = "temp_r";
    public static final String v = "setaudioin.cgi";
    public static final String v0 = "setRemoveEdogPackage.cgi";
    public static final String v1 = "type";
    private static final String v2 = "mfrs_lf";
    public static final String w = "setscreenautosleep.cgi";
    public static final String w0 = "setEdogPackage.cgi";
    public static final String w1 = "start";
    private static final String w2 = "mfrs_rf";
    public static final String x = "setsoundcontrol.cgi";
    public static final String x0 = "getspeedunit.cgi";
    public static final String x1 = "end";
    private static final String x2 = "mfrs_lr";
    public static final String y = "setcollision.cgi";
    public static final String y0 = "setspeedunit.cgi";
    public static final String y1 = "name";
    private static final String y2 = "mfrs_rr";
    public static final String z = "setemergencysens.cgi";
    public static final String z0 = "getdateformat.cgi";
    public static final String z1 = "path";
    private static final String z2 = "tpms_id_lf";

    public static b0<String> A(Context context, String str) {
        return c(context, p, new c(l2, str));
    }

    public static b0<String> A0(Context context) {
        return c(context, q1, new c[0]);
    }

    public static b0<String> A1(Context context) {
        return c(context, V0, new c[1]);
    }

    public static b0<String> B(Context context) {
        return c(context, r, new c[0]);
    }

    public static b0<String> B0(Context context, String str) {
        return c(context, i1, new c(T2, str));
    }

    public static b0<String> B1(Context context, String str, String str2, String str3, String str4) {
        return c(context, P0, new c(v2, "BHSENS"), new c(z2, str), new c(w2, "BHSENS"), new c(A2, str2), new c(x2, "BHSENS"), new c(B2, str3), new c(y2, "BHSENS"), new c(C2, str4));
    }

    public static b0<String> C(Context context) {
        return c(context, "getparkingattr.cgi", new c[0]);
    }

    public static b0<String> C0(Context context, String str) {
        return c(context, h1, new c(R2, str));
    }

    public static b0<String> C1(Context context, String str, String str2, String str3, String str4) {
        c[] cVarArr = new c[2];
        if (!TextUtils.isEmpty(str)) {
            cVarArr[0] = new c(J2, str);
            cVarArr[1] = new c(K2, str2);
        } else {
            cVarArr[0] = new c(L2, str3);
            cVarArr[1] = new c(M2, str4);
        }
        return c(context, d1, cVarArr);
    }

    public static b0<String> D(Context context) {
        return c(context, Z0, new c[0]);
    }

    public static b0<String> D0(Context context, String str) {
        return c(context, i1, new c(U2, str));
    }

    public static String D1(BaseDeviceActivity baseDeviceActivity) {
        return "http://" + I1() + "/sd";
    }

    public static b0<String> E(Context context) {
        return c(context, "getparkingattr.cgi", new c[0]);
    }

    public static b0<String> E0(Context context, String str) {
        return c(context, i1, new c(S2, str));
    }

    public static String E1() {
        return "http://" + I1() + "/cgi-bin/fileupload.cgi";
    }

    public static b0<String> F(Context context) {
        return c(context, T, new c[0]);
    }

    public static b0<String> F0(Context context, String str) {
        return c(context, E, new c(I1, str));
    }

    public static String F1(Context context, String str) {
        return a(context, o0, new c(r1, str), new c(s1, new BanyacKeyUtils().b(-1L, (Long) null, str)));
    }

    public static b0<String> G(Context context) {
        return c(context, T0, new c[0]);
    }

    public static b0<String> G0(Context context, String str) {
        return c(context, E, new c(N1, str));
    }

    public static b0<String> G1(Context context, String str) {
        return c(context, l1, new c(W2, str));
    }

    public static b0<String> H(Context context) {
        return c(context, C, new c(D1, "0"), new c("type", "0"));
    }

    public static b0<String> H0(Context context, String str) {
        return c(context, E, new c(N1, str));
    }

    @m0
    private static StringBuilder H1() {
        StringBuilder sb = new StringBuilder();
        sb.append("http://");
        sb.append(I1());
        sb.append("/");
        return sb;
    }

    public static b0<String> I(Context context) {
        return c(context, B, new c(D1, "0"), new c("type", "0"));
    }

    public static b0<String> I0(Context context, String str) {
        return c(context, E, new c(G1, str));
    }

    public static String I1() {
        return r.e();
    }

    public static b0<String> J(Context context) {
        return c(context, H, new c[0]);
    }

    public static b0<String> J0(Context context, String str) {
        return c(context, E, new c(H1, str));
    }

    public static String J1(HisiFileNode hisiFileNode) {
        StringBuilder H12 = H1();
        H12.append(hisiFileNode.getPath().replace(d, e));
        H12.append("/");
        H12.append(hisiFileNode.getName().replace(f, g));
        return H12.toString();
    }

    public static b0<String> K(Context context) {
        return c(context, H0, new c[0]);
    }

    public static b0<String> K0(Context context, String str) {
        return c(context, "setlapserecattr.cgi", new c(N1, str));
    }

    public static long K1(HisiFileNode hisiFileNode) {
        return Long.valueOf(hisiFileNode.getSize()).longValue();
    }

    public static b0<String> L(Context context) {
        return c(context, M0, new c[0]);
    }

    public static b0<String> L0(Context context, String str, String str2) {
        return c(context, S0, new c(r2, str), new c(s2, str2));
    }

    public static String L1(HisiFileNode hisiFileNode) {
        int lastIndexOf = hisiFileNode.getName().lastIndexOf("-");
        if (lastIndexOf > 14) {
            return hisiFileNode.getName().substring(lastIndexOf - 15, lastIndexOf);
        }
        return null;
    }

    public static b0<String> M(Context context) {
        return c(context, Q0, new c[0]);
    }

    public static b0<String> M0(Context context, String str, String str2, String str3, String str4, String str5) {
        return c(context, w0, new c(N1, str), new c(g2, str2), new c(h2, str3), new c(i2, str4), new c(R1, str5));
    }

    public static String M1(HisiFileNode hisiFileNode) {
        int lastIndexOf = hisiFileNode.getName().lastIndexOf("-");
        if (lastIndexOf > 14) {
            return hisiFileNode.getName().substring(lastIndexOf - 15, lastIndexOf - 2);
        }
        return null;
    }

    public static b0<String> N(Context context) {
        return c(context, U0, new c[1]);
    }

    public static b0<String> N0(Context context, String str) {
        return c(context, Z, new c(N1, str));
    }

    public static boolean N1(HisiFileNode hisiFileNode) {
        String substring = hisiFileNode.getName().substring(hisiFileNode.getName().lastIndexOf("."));
        if (substring.equals(".JPG")) {
            return false;
        }
        return substring.equals(".MP4");
    }

    public static b0<String> O(Context context) {
        return c(context, t0, new c[0]);
    }

    public static b0<String> O0(Context context, String str) {
        return c(context, c0, new c(j2, str));
    }

    public static String O1(HisiFileNode hisiFileNode) {
        StringBuilder sb = new StringBuilder();
        sb.append("http://");
        sb.append(I1());
        sb.append("/");
        sb.append(hisiFileNode.getPath());
        sb.append("/");
        sb.append((CharSequence) hisiFileNode.getName(), 0, hisiFileNode.getName().lastIndexOf("."));
        sb.append(".THM");
        return sb.toString();
    }

    public static b0<String> P(Context context, String str) {
        return c(context, D0, new c(o2, str));
    }

    public static b0<String> P0(Context context, String str) {
        return c(context, v0, new c(g2, str));
    }

    public static String P1(HisiFileNode hisiFileNode) {
        return "http://" + I1() + "/" + hisiFileNode.getPath() + "/" + hisiFileNode.getName();
    }

    public static b0<String> Q(Context context) {
        return c(context, s, new c[0]);
    }

    public static b0<String> Q0(Context context, String str, String str2) {
        return c(context, D, new c(D1, "0"), new c("type", "0"), new c(E1, str2), new c(F1, str));
    }

    public static String Q1(String str, HisiFileNode hisiFileNode, DashCam dashCam) {
        StringBuilder sb = new StringBuilder();
        sb.append("http://");
        sb.append(I1());
        sb.append("/");
        if ("MAIHisiDashCam".equals(str)) {
            sb.append(hisiFileNode.getPath());
            sb.append("_s/");
            sb.append((CharSequence) hisiFileNode.getName(), 0, hisiFileNode.getName().lastIndexOf("."));
            sb.append("_s.MP4");
        } else if (dashCam.isUseSmallVideo()) {
            String path = hisiFileNode.getPath();
            if (path.contains("/Front")) {
                path = path.replace("/Front", "/.s_Front");
            }
            sb.append(path);
            sb.append("/");
            sb.append((CharSequence) hisiFileNode.getName(), 0, hisiFileNode.getName().lastIndexOf("."));
            sb.append(".MP4");
        } else if ("Mai16HisDashCam".equals(str)) {
            String path2 = hisiFileNode.getPath();
            if (path2.contains("/Normal")) {
                path2 = path2.replace("/Normal", "/.s_Normal");
            } else if (path2.contains("/Lapse")) {
                path2 = path2.replace("/Lapse", "/.s_Lapse");
            } else if (path2.contains("/Event")) {
                path2 = path2.replace("/Event", "/.s_Event");
            } else if (path2.contains("/Parking")) {
                path2 = path2.replace("/Parking", "/.s_Parking");
            }
            sb.append(path2);
            sb.append("/");
            sb.append((CharSequence) hisiFileNode.getName(), 0, hisiFileNode.getName().lastIndexOf("."));
            sb.append(".MP4");
        } else if (!"Mai1500HisiDashCam".equals(str) && !"Mai1500HisiDashCamIntl".equals(str) && !"Mai2200HisiDashCam".equals(str) && !"Mai2200HisiDashCamIntl".equals(str)) {
            sb.append(hisiFileNode.getPath());
            sb.append("/");
            sb.append((CharSequence) hisiFileNode.getName(), 0, hisiFileNode.getName().lastIndexOf("."));
            sb.append(".MP4");
        } else {
            sb.append("/");
            String[] split = hisiFileNode.getPath().split("/");
            for (int i3 = 0; i3 < split.length; i3++) {
                if (i3 == split.length - 1) {
                    sb.append(".s_");
                    sb.append(split[i3]);
                    sb.append("/");
                } else {
                    sb.append(split[i3]);
                    sb.append("/");
                }
            }
            sb.append((CharSequence) hisiFileNode.getName(), 0, hisiFileNode.getName().lastIndexOf("."));
            sb.append(".MP4");
        }
        return sb.toString();
    }

    public static b0<String> R(Context context) {
        return c(context, h, new c[0]);
    }

    public static b0<String> R0(Context context, String str) {
        return c(context, g0, new c(K1, str));
    }

    public static String R1(HisiFileNode hisiFileNode) {
        return "http://" + I1() + "/" + hisiFileNode.getPath().replace("s_", "") + "/" + hisiFileNode.getName().substring(0, hisiFileNode.getName().lastIndexOf(".")) + ".RSD";
    }

    public static b0<String> S(Context context, String str) {
        return c(context, I0, new c(N1, str));
    }

    public static b0<String> S0(Context context, String str) {
        return c(context, c1, new c("type", str));
    }

    public static String S1(String str, HisiFileNode hisiFileNode) {
        StringBuilder sb = new StringBuilder();
        if ("MAIHisiDashCam".equals(str)) {
            sb.append("http://");
            sb.append(I1());
            sb.append("/");
            sb.append(hisiFileNode.getPath());
            sb.append("_s/");
            sb.append((CharSequence) hisiFileNode.getName(), 0, hisiFileNode.getName().lastIndexOf("."));
            sb.append("_s.THM");
        } else if (!"Mai1500HisiDashCam".equals(str) && !"Mai1500HisiDashCamIntl".equals(str) && !"Mai2200HisiDashCam".equals(str) && !"Mai2200HisiDashCamIntl".equals(str)) {
            sb.append("http://");
            sb.append(I1());
            sb.append("/");
            sb.append(hisiFileNode.getPath());
            sb.append("/");
            sb.append((CharSequence) hisiFileNode.getName(), 0, hisiFileNode.getName().lastIndexOf("."));
            sb.append(".THM");
        } else {
            sb.append("http://");
            sb.append(I1());
            sb.append("/");
            String[] split = hisiFileNode.getPath().split("/");
            for (int i3 = 0; i3 < split.length; i3++) {
                if (i3 == split.length - 1) {
                    sb.append(".s_");
                    sb.append(split[i3]);
                    sb.append("/");
                } else {
                    sb.append(split[i3]);
                    sb.append("/");
                }
            }
            sb.append((CharSequence) hisiFileNode.getName(), 0, hisiFileNode.getName().lastIndexOf("."));
            sb.append(".THM");
        }
        return sb.toString();
    }

    public static b0<String> T(Context context) {
        return c(context, b0, new c[1]);
    }

    public static b0<String> T0(Context context, String str) {
        return c(context, h0, new c("time", str));
    }

    public static String T1(HisiFileNode hisiFileNode) {
        return "http://" + I1() + "/" + hisiFileNode.getPath() + "/" + hisiFileNode.getName();
    }

    public static b0<String> U(Context context) {
        return c(context, l, new c[0]);
    }

    public static b0<String> U0(Context context, String str) {
        return c(context, w, new c("time", str));
    }

    public static b0<String> V(Context context) {
        return c(context, a0, new c[1]);
    }

    public static b0<String> V0(Context context, String str) {
        return c(context, g1, new c(N1, str));
    }

    public static b0<String> W(Context context, boolean z3) {
        c[] cVarArr = new c[1];
        cVarArr[0] = new c(t1, z3 ? w1 : l2);
        return c(context, i, cVarArr);
    }

    public static b0<String> W0(Context context, String str) {
        return c(context, x, new c(K1, str));
    }

    public static b0<String> X(Context context) {
        return c(context, O, new c[1]);
    }

    public static b0<String> X0(Context context, String str) {
        return c(context, y0, new c(m2, str));
    }

    public static b0<String> Y(Context context, String str) {
        return c(context, J0, new c(N1, str));
    }

    public static b0<String> Y0(Context context, String str) {
        return c(context, N0, new c(b3, str));
    }

    public static b0<String> Z(Context context) {
        return c(context, I, new c(J1, "1"));
    }

    public static b0<String> Z0(Context context) {
        return c(context, j, new c("time", new SimpleDateFormat("yyyyMMddHHmmss").format(Calendar.getInstance().getTime())));
    }

    public static String a(Context context, String str, c... cVarArr) {
        return b(context, false, str, cVarArr);
    }

    public static String a0(Context context, boolean z3, String str) {
        c[] cVarArr = new c[2];
        cVarArr[0] = new c(q2, str);
        return b(context, z3, O0, cVarArr);
    }

    public static b0<String> a1(Context context, String str) {
        return c(context, j, new c("time", str));
    }

    public static String b(Context context, boolean z3, String str, c... cVarArr) {
        StringBuilder sb = new StringBuilder();
        sb.append("http://");
        if (z3) {
            sb.append("127.0.0.1:" + c);
        } else {
            sb.append(I1());
        }
        sb.append("/cgi-bin/");
        sb.append(str);
        if (cVarArr != null && cVarArr.length > 0) {
            sb.append("?");
            for (c cVar : cVarArr) {
                if (cVar != null) {
                    sb.append(cVar.a());
                }
            }
        }
        return sb.toString();
    }

    public static b0<String> b0(Context context, String str) {
        return c(context, e1, new c(N1, str));
    }

    public static b0<String> b1(Context context, String str, String str2) {
        return c(context, R0, new c(t2, str), new c(u2, str2));
    }

    public static b0<String> c(Context context, String str, c... cVarArr) {
        b0<String> l3;
        String str2 = b;
        String str3 = "wifi";
        if (str2 != null) {
            l3 = b0.l3(str2);
            str3 = "4G";
        } else if (MainActivity.r1 != null) {
            if (TextUtils.isEmpty(MainActivity.q1)) {
                l3 = d(context, MainActivity.r1, "wifi");
            } else {
                l3 = b0.l3(MainActivity.q1);
            }
        } else {
            String str4 = MainActivity.q1;
            if (str4 == null) {
                str4 = "";
            }
            l3 = b0.l3(str4);
        }
        return l3.z3(new b(str3, str, cVarArr));
    }

    public static b0<String> c0(Context context, String str) {
        return c(context, v, new c(N1, str));
    }

    public static b0<String> c1(Context context, String str) {
        return c(context, p0, new c(f2, str));
    }

    public static b0<String> d(Context context, String str, String str2) {
        return b0.q1(new a(context, str, str2));
    }

    public static b0<String> d0(Context context, String str) {
        return c(context, A, new c(K1, str));
    }

    public static b0<String> d1(Context context, String str, String str2) {
        return c(context, b1, new c(N2, str), new c(O2, str2));
    }

    public static b0<String> e(Context context, String str, String str2) {
        return c(context, Y0, new c(D2, str), new c(E2, str2));
    }

    public static b0<String> e0(Context context, String str) {
        return c(context, m0, new c(N1, str));
    }

    public static b0<String> e1(Context context, String str) {
        return c(context, D, new c(D1, "0"), new c("type", "0"), new c(F1, str));
    }

    public static b0<String> f(Context context) {
        return c(context, G0, new c[0]);
    }

    public static b0<String> f0(Context context, String str) {
        return c(context, X, new c(N1, str));
    }

    public static b0<String> f1(Context context, String str) {
        return c(context, V, new c(N1, str));
    }

    public static b0<String> g(Context context) {
        return c(context, x0, new c[0]);
    }

    public static b0<String> g0(Context context, String str) {
        return c(context, K0, new c(N1, str));
    }

    public static b0<String> g1(Context context, String str) {
        return c(context, k0, new c(a3, str));
    }

    public static String h(Context context, String str) {
        return a(context, n0, new c(k2, str), new c(s1, new BanyacKeyUtils().b(-1L, (Long) null, str)));
    }

    public static b0<String> h0(Context context, String str) {
        return c(context, u, new c(N1, str));
    }

    public static b0<String> h1(Context context, String str) {
        return c(context, k1, new c(V2, str));
    }

    public static b0<String> i(Context context, boolean z3, String str) {
        c[] cVarArr = new c[2];
        cVarArr[0] = new c(L1, z3 ? "register" : "unregister");
        cVarArr[1] = new c(M1, str);
        return c(context, J, cVarArr);
    }

    public static b0<String> i0(Context context, String str) {
        return c(context, p1, new c(N1, str));
    }

    public static b0<String> i1(Context context, String str) {
        return c(context, d0, new c(N1, str));
    }

    public static b0<String> j(Context context, String str, String str2) {
        return c(context, q, new c(z1, str), new c(y1, str2));
    }

    public static b0<String> j0(Context context, String str) {
        return c(context, y, new c(K1, str));
    }

    public static b0<String> j1(Context context) {
        return c(context, C0, new c[0]);
    }

    public static b0<String> k(Context context, String str) {
        return c(context, z, new c(P2, str));
    }

    public static b0<String> k0(Context context, String str) {
        return c(context, L0, new c(N1, str));
    }

    public static b0<String> k1(Context context, String str) {
        return c(context, t, new c(A1, str));
    }

    public static b0<String> l(Context context, String str) {
        return c(context, e0, new c(N1, str));
    }

    public static b0<String> l0(Context context, String str) {
        return c(context, A0, new c("type", str));
    }

    public static b0<String> l1(Context context, String str) {
        return c(context, t, new c(B1, str));
    }

    public static b0<String> m(Context context) {
        return c(context, f1, new c[0]);
    }

    public static b0<String> m0(Context context, String str, String str2) {
        c[] cVarArr = new c[1];
        if (str != null) {
            cVarArr[0] = new c(F2, str);
        }
        if (str2 != null) {
            cVarArr[0] = new c(G2, str2);
        }
        return c(context, X0, cVarArr);
    }

    public static b0<String> m1(Context context, String str) {
        return c(context, M, new c(N1, str));
    }

    public static b0<String> n(Context context) {
        return c(context, Q, new c[0]);
    }

    public static b0<String> n0(Context context, String str) {
        return c(context, n1, new c(Y2, str));
    }

    public static b0<String> n1(Context context, boolean z3) {
        c[] cVarArr = new c[1];
        cVarArr[0] = new c(N1, z3 ? "0" : "1");
        return c(context, K, cVarArr);
    }

    public static b0<String> o(Context context) {
        return c(context, Y, new c[0]);
    }

    public static b0<String> o0(Context context, String str) {
        return c(context, m1, new c(X2, str));
    }

    public static b0<String> o1(Context context) {
        return c(context, E0, new c[0]);
    }

    public static b0<String> p(Context context) {
        return c(context, z0, new c[0]);
    }

    public static b0<String> p0(Context context, String str) {
        return c(context, B0, new c(N1, str));
    }

    public static b0<String> p1(Context context, String str) {
        return c(context, P, new c(S1, str));
    }

    public static b0<String> q(Context context, String str, String str2) {
        c[] cVarArr = new c[2];
        cVarArr[0] = new c(H2, str);
        if (!TextUtils.isEmpty(str2)) {
            cVarArr[1] = new c("type", str2);
        }
        return c(context, W0, cVarArr);
    }

    public static b0<String> q0(Context context, String str) {
        return c(context, s0, new c(N1, str));
    }

    public static b0<String> q1(Context context, String str) {
        return c(context, P, new c(T1, str));
    }

    public static b0<String> r(Context context) {
        return c(context, a1, new c[0]);
    }

    public static b0<String> r0(Context context, String str) {
        return c(context, j1, new c(Q2, str));
    }

    public static b0<String> r1(Context context, String str) {
        return c(context, P, new c(V1, str));
    }

    public static b0<String> s(Context context) {
        return c(context, F0, new c[0]);
    }

    public static b0<String> s0(Context context, String str) {
        return c(context, l0, new c("type", str));
    }

    public static b0<String> s1(Context context, String str) {
        return c(context, P, new c(W1, str));
    }

    public static b0<String> t(Context context) {
        return c(context, S, new c[0]);
    }

    public static b0<String> t0(Context context, String str) {
        return c(context, f0, new c(e2, str));
    }

    public static b0<String> t1(Context context, String str) {
        return c(context, P, new c(U1, str));
    }

    public static b0<String> u(Context context) {
        return c(context, u0, new c[0]);
    }

    public static b0<String> u0(Context context, String str) {
        return c(context, "setlapserecattr.cgi", new c(N1, str));
    }

    public static b0<String> u1(Context context, String str) {
        return c(context, P, new c(X1, str));
    }

    public static b0<String> v(Context context) {
        return c(context, m, new c[0]);
    }

    public static b0<String> v0(Context context, String str) {
        return c(context, i0, new c(N1, str));
    }

    public static b0<String> v1(Context context, String str) {
        return c(context, P, new c(Y1, str));
    }

    public static b0<String> w(Context context, String str) {
        return c(context, m, new c("type", str));
    }

    public static b0<String> w0(Context context, String str) {
        return c(context, o1, new c(Z2, str));
    }

    public static b0<String> w1(Context context, String str) {
        return c(context, R, new c(Z1, str));
    }

    public static b0<String> x(Context context, String str, int i3, int i4) {
        return c(context, n, new c(w1, String.valueOf(i3)), new c(x1, String.valueOf(i4)), new c("type", str));
    }

    public static b0<String> x0(Context context, boolean z3, String str, String str2, String str3, String str4) {
        c[] cVarArr = new c[5];
        cVarArr[0] = new c(N1, z3 ? "0" : "1");
        cVarArr[1] = new c(O1, str);
        cVarArr[2] = new c(P1, str2);
        cVarArr[3] = new c(Q1, str3);
        cVarArr[4] = new c(R1, str4);
        return c(context, L, cVarArr);
    }

    public static b0<String> x1(Context context, String str) {
        return c(context, R, new c(a2, str));
    }

    public static b0<String> y(Context context) {
        return c(context, o, new c[0]);
    }

    public static b0<String> y0(Context context, boolean z3, String str, String str2, String str3, String str4) {
        c[] cVarArr = new c[5];
        cVarArr[0] = new c(N1, z3 ? "0" : "1");
        cVarArr[1] = new c(O1, str);
        cVarArr[2] = new c(P1, str2);
        cVarArr[3] = new c(i2, String.valueOf(str3));
        cVarArr[4] = new c(R1, str4);
        return c(context, L, cVarArr);
    }

    public static b0<String> y1(Context context, String str) {
        return c(context, R, new c(b2, str));
    }

    public static b0<String> z(Context context) {
        return c(context, U, new c[0]);
    }

    public static b0<String> z0(Context context, String str) {
        return c(context, W, new c(d2, str));
    }

    public static b0<String> z1(Context context, String str) {
        return c(context, R, new c(c2, str));
    }
}
