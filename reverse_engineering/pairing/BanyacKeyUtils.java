package com.banyac.key;
/* loaded from: /tmp/jadx-1127059114916393541.dex */
public class BanyacKeyUtils {
    public static void a() {
        System.loadLibrary("banyackey");
    }

    private native String sign(long j, String str);

    public String b(long j, Long l, String str) {
        if (l != null) {
            return sign(j, str + l);
        }
        return sign(j, str);
    }
}
