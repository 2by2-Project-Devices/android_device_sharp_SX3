#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/sharp/SX3',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/motorola',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libtflite_mtk',
        'libneuron_graph_delegate.mtk',
        'vendor.mediatek.hardware.apuware.apusys@2.0',
        'vendor.mediatek.hardware.apuware.apusys@2.1',
        'vendor.mediatek.hardware.apuware.hmp@1.0',
        'vendor.mediatek.hardware.apuware.utils@2.0',
        'vendor.mediatek.hardware.videotelephony@1.0',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    #'system_ext/priv-app/ImsService/ImsService.apk': blob_fixup()
    #    .apktool_patch('patches/ImsService/'),
    #'system_ext/priv-app/MtkGbaService/MtkGbaService.apk': blob_fixup()
    #    .apktool_patch('patches/GbaService'),
    'system_ext/lib64/libimsma.so': blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),
    'system_ext/lib64/libsink-mtk.so': blob_fixup()
        .add_needed('libaudioclient_shim.so'),
    'vendor/lib64/hw/audio.primary.mediatek.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libutils.so','libutils-v32.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v31.so')
        .replace_needed('libalsautils.so','libalsautils-v31.so'),
    ('vendor/bin/mnld', 'vendor/lib64/mt6833/libaalservice.so', 'vendor/lib64/mt6833/libcam.utils.sensorprovider.so', 'vendor/lib64/librgbwlightsensor.so'): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so')
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),
    ('vendor/lib64/libaalservice.so', 'vendor/lib64/libcam.utils.sensorprovider.so'): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so')
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),
    (
        'vendor/lib64/hw/mt6833/android.hardware.camera.provider@2.6-impl-mediatek.so',
        'vendor/lib64/mt6833/libmtkcam_stdutils.so',
        'vendor/bin/hw/vendor.dolby.media.c2@1.0-service',
    ): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    ('vendor/lib64/librt_extamp_intf.so', 'vendor/lib64/libpqxmlparser.so'): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v31.so'),
    'vendor/lib64/hw/mt6833/vendor.mediatek.hardware.pq_aidl-impl.so': blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v31.so')
        .replace_needed('libutils.so', 'libutils-v32.so')
        .add_needed('android.hardware.sensors@1.0-convert-shared.so'),
    'vendor/bin/hw/mtkfusionrild': blob_fixup()
        .add_needed('libutils-v32.so'),
    ('vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so', 'vendor/bin/hw/android.hardware.gnss-service.mediatek'): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    ('vendor/lib64/hw/hwcomposer.mtk_common.so', 'vendor/lib64/mt6833/libcam.hal3a.v3.so'): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    ('vendor/lib64/mt6833/lib3a.flash.so', 'vendor/lib64/mt6833/lib3a.ae.stat.so',
     'vendor/lib64/mt6833/lib3a.sensors.flicker.so', 'vendor/lib64/mt6833/lib3a.sensors.color.so',
     'vendor/lib64/lib3a.ae.pipe.so'): blob_fixup()
        .add_needed('liblog.so'),
    ('vendor/lib64/mt6833/libneuralnetworks_sl_driver_mtk_prebuilt.so', 
     'vendor/lib64/libstfactory-vendor.so', 'vendor/lib64/libnvram.so',
     'vendor/lib64/libsysenv.so', 'vendor/lib64/libtflite_mtk.so', 'vendor/lib64/sensors.moto.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    ('vendor/bin/hw/android.hardware.security.keymint@2.0-service.trustonic', 'vendor/lib64/libtpa.so'): blob_fixup()
        .replace_needed('android.hardware.security.keymint-V1-ndk_platform.so', 'android.hardware.security.keymint-V1-ndk.so')
        .replace_needed('android.hardware.security.secureclock-V1-ndk_platform.so', 'android.hardware.security.secureclock-V1-ndk.so')
        .replace_needed('android.hardware.security.sharedsecret-V1-ndk_platform.so', 'android.hardware.security.sharedsecret-V1-ndk.so')
        .add_needed('android.hardware.security.rkp-V3-ndk.so')
        .add_needed('libbase_shim.so'),
    'vendor/lib64/mt6833/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),
    'vendor/etc/libnfc-nxp_220.conf': blob_fixup()
        .regex_replace('DEFAULT_ISODEP_ROUTE=0x01', 'DEFAULT_ISODEP_ROUTE=0xC0')
        .regex_replace('DEFAULT_SYS_CODE_ROUTE=0x01', 'DEFAULT_SYS_CODE_ROUTE=0xC0')
        .regex_replace('DEFAULT_OFFHOST_ROUTE=0x01', 'DEFAULT_OFFHOST_ROUTE=0xC0')
        .regex_replace('OFFHOST_ROUTE_ESE={01}', 'OFFHOST_ROUTE_ESE={C0}')
        .add_line_if_missing('DEFAULT_NFCF_ROUTE=0xC0'),
    (
        'vendor/lib64/libcodec2_soft_ac4dec.so',
        'vendor/lib64/libcodec2_soft_ddpdec.so',
        'vendor/lib64/libdlbdsservice.so',
        'vendor/lib64/libdlbpreg.so',
        'vendor/lib64/soundfx/libdlbvol.so',
    ): blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'vendor/lib64/soundfx/libswdap.so': blob_fixup()
        .binary_regex_replace(b'\x1f\x00\x00\x71\xe0\x03\x00\x91\xf3\x17\x9f\x1a\x41\x62\x04\x94',
                              b'\x1f\x00\x00\x71\xe0\x03\x00\x91\x13\x00\x80\x52\x41\x62\x04\x94')
        .binary_regex_replace(rb'\x09\x00\x00\x12\x89\x02\x09\x0b\x3f\x01\x08\x6b\xca\x01\x00\x54',
                              b'\x09\x00\x00\x12\x89\x02\x09\x0b\x3f\x01\x08\x6b\x0e\x00\x00\x14')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'system_ext/lib64/libgpud_sys.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so')
        .replace_needed('android.hardware.graphics.common-V6-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    'vendor/lib64/librilfusion.so': blob_fixup()
        .replace_needed('android.hardware.radio.sim-V2-ndk.so', 'android.hardware.radio.sim-V1-ndk.so')
        .replace_needed('android.hardware.radio.config-V2-ndk.so', 'android.hardware.radio.config-V1-ndk.so'),
    'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V1-ndk.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V3-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    ('vendor/lib64/libcodec2_vpp_AISR_plugin.so',
     'vendor/lib64/libcodec2_vpp_AIMEMC_plugin.so'): blob_fixup()
        .replace_needed('android.hardware.graphics.allocator-V1-ndk.so', 'android.hardware.graphics.allocator-V2-ndk.so')
        .replace_needed('android.hardware.graphics.common-V3-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    'vendor/lib64/libtpa.so': blob_fixup()
        .replace_needed('android.hardware.security.keymint-V2-ndk.so', 'android.hardware.security.keymint-V4-ndk.so'),
    ('vendor/lib64/libmtk-ril.so', 'vendor/lib64/libmtkmipc-ril.so'): blob_fixup()
        .replace_needed('libtflite.so', 'libtflite-v33.so'),
    'vendor/bin/hw/android.hardware.usb-aidl-service.mediatekv1.0': blob_fixup()
        .add_needed('libbase_shim.so'),
    'vendor/etc/init/hw/init.vendor.st21nfc.rc': blob_fixup()
        .regex_replace('libnfc-nci-st-felica.conf', 'libnfc-hal-st-felica.conf'),



    ('system_ext/etc/init/init.vtservice.rc', 'vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc'): blob_fixup()
        .regex_replace('start', 'enable'),
    'system_ext/lib64/libimsma.so': blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),
    'system_ext/lib64/libsink-mtk.so': blob_fixup()
        .add_needed('libaudioclient_shim.so'),
    'system_ext/lib64/libsource.so': blob_fixup()
        .add_needed('libui_shim.so'),
    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so'),
    ('vendor/bin/mnld', 'vendor/lib64/hw/android.hardware.sensors@2.X-subhal-mediatek.so', 'vendor/lib64/mt6897/libcam.utils.sensorprovider.so'): blob_fixup()
        .add_needed('android.hardware.sensors@1.0-convert-shared.so'),
    'vendor/lib64/hw/audio.primary.mediatek.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libutils.so','libutils-v32.so')
        .replace_needed('libalsautils.so','libalsautils-v31.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    'vendor/lib64/hw/hwcomposer.mtk_common.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    ('vendor/lib64/mt6897/libneuralnetworks_sl_driver_mtk_prebuilt.so',
     'vendor/lib64/libstfactory-vendor.so', 'vendor/lib64/libnvram.so',
     'vendor/lib64/libsysenv.so', 'vendor/lib64/libtflite_mtk.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    ('vendor/lib64/hw/mt6897/android.hardware.camera.provider@2.6-impl-mediatek.so','vendor/lib64/mt6897/libmtkcam_stdutils.so',
     'vendor/lib64/sensors.moto.so'): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .add_needed('libbase_shim.so'),
    'vendor/etc/vintf/manifest/manifest_media_c2_V1_2_default.xml': blob_fixup()
        .regex_replace('1.1', '1.2')
        .regex_replace('@1.0', '@1.2')
        .regex_replace('default9', 'default'),
    ('vendor/lib64/mt6897/lib3a.flash.so', 'vendor/lib64/mt6897/lib3a.ae.stat.so',
     'vendor/lib64/mt6897/lib3a.sensors.flicker.so', 'vendor/lib64/mt6897/lib3a.sensors.color.so',
     'vendor/lib64/lib3a.ae.pipe.so'): blob_fixup()
        .add_needed('liblog.so'),
    'vendor/lib64/mt6897/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),
    'vendor/bin/hw/android.hardware.biometrics.fingerprint-service.fpc': blob_fixup()
        .binary_regex_replace(b'/virtual', b'/default')
        .replace_needed('android.hardware.biometrics.common-V3-ndk.so', 'android.hardware.biometrics.common-V4-ndk.so')
        .replace_needed('android.hardware.biometrics.fingerprint-V3-ndk.so', 'android.hardware.biometrics.fingerprint-V4-ndk.so'),
    'vendor/etc/vintf/manifest/manifest_IMoto_AIDL_Fingerprint.xml': blob_fixup()
        .regex_replace('IFingerprint/virtual', 'IFingerprint/default'),
    'vendor/lib64/mt6897/libmtkcam_hal_aidl_common.so': blob_fixup()
        .replace_needed('android.hardware.camera.common-V2-ndk.so', 'android.hardware.camera.common-V1-ndk.so'),
    'vendor/lib64/libmtkcam_hal_aidl_common.so': blob_fixup()
        .replace_needed('android.hardware.camera.common-V2-ndk.so', 'android.hardware.camera.common-V1-ndk.so'),
    'vendor/lib64/vendor.mediatek.hardware.bluetooth.audio-V1-ndk.so': blob_fixup()
        .replace_needed('android.hardware.audio.common-V1-ndk.so', 'android.hardware.audio.common-V2-ndk.so'),
    'vendor/lib64/mt6897/libpqconfig.so': blob_fixup()
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),
    ('vendor/lib64/mt6897/lib3a.ae.stat.so',
     'vendor/lib64/libarmnn_ndk.mtk.vndk.so'): blob_fixup()
        .add_needed('liblog.so'),
    ('vendor/bin/hw/mt6897/android.hardware.graphics.allocator-V2-service-mediatek.mt6897',
     'vendor/lib64/egl/mt6897/libGLES_mali.so',
     'vendor/lib64/hw/mt6897/android.hardware.graphics.allocator-V2-mediatek.so',
     'vendor/lib64/hw/mt6897/android.hardware.graphics.mapper@4.0-impl-mediatek.so',
     'vendor/lib64/hw/mt6897/mapper.mediatek.so',
     'vendor/lib64/mt6897/libmtkcam_grallocutils.so',
     'vendor/lib64/libcodec2_fsr.so',
     'vendor/lib64/libmtkcam_grallocutils_aidlv1helper.so',
     'vendor/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so',
     'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
     'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V4-ndk.so',
     'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V7-ndk.so'): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V4-ndk.so', 'android.hardware.graphics.common-V7-ndk.so')
        .replace_needed('android.hardware.graphics.allocator-V1-ndk.so', 'android.hardware.graphics.allocator-V2-ndk.so'),
    'vendor/lib64/mt6897/libneuralnetworks_sl_driver_mtk_prebuilt.so': blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_createFromHandle')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_getNativeHandle')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'vendor/lib64/hw/mt6897/vendor.mediatek.hardware.pq_aidl-impl.so': blob_fixup()
        .add_needed('libui_shim.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    'vendor/etc/init/hw/init.vendor.st21nfc.rc': blob_fixup()
        .regex_replace('libnfc-nci-st-felica.conf', 'libnfc-hal-st-felica.conf'),
    'vendor/etc/init/thermal-mediatek.rc': blob_fixup()
        .regex_replace('android.hardware.thermal-service.mediatek', 'android.hardware.thermal-service.mediatek.fuji'),
    'system_ext/lib64/libgpud_sys.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V6-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    ('vendor/lib64/mt6897/libmmlpqImpl.so',
     'vendor/lib64/libpqxmlflagparser.so',
     'vendor/lib64/libpqxmlparser.so',
     'vendor/lib64/librt_extamp_intf.so',
     'vendor/lib64/libsilkybrightnesscore.so'): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b': blob_fixup()
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v34.so')
        .replace_needed('libcodec2_hidl@1.1.so', 'libcodec2_hidl@1.1-v34.so')
        .replace_needed('libcodec2_hidl@1.2.so', 'libcodec2_hidl@1.2-v34.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v34.so'),
    'vendor/lib64/libcodec2_fsr.so': blob_fixup()
        .replace_needed('libui.so', 'libui-v34.so')
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    ('vendor/lib64/libgpud.so', 'vendor/lib64/libmtkcam_grallocutils.so'): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    ('vendor/lib64/egl/libGLES_mali.so',
     'vendor/lib64/hw/android.hardware.graphics.allocator-V2-mediatek.so',
     'vendor/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so',
     'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
     'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V4-ndk.so',
     'vendor/bin/hw/android.hardware.graphics.allocator-V2-service-mediatek'): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    'vendor/lib64/libcodec2_hidl@1.0-v34.so': blob_fixup()
        .replace_needed('libstagefright_bufferqueue_helper.so', 'libstagefright_bufferqueue_helper-v35.so')
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v34.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v34.so')
        .replace_needed('libui.so', 'libui-v34.so'),
    'vendor/lib64/libcodec2_hidl@1.1-v34.so': blob_fixup()
        .replace_needed('libstagefright_bufferqueue_helper.so', 'libstagefright_bufferqueue_helper-v35.so')
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v34.so')
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v34.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v34.so')
        .replace_needed('libui.so', 'libui-v34.so'),
    'vendor/lib64/libcodec2_hidl@1.2-v34.so': blob_fixup()
        .replace_needed('libstagefright_bufferqueue_helper.so', 'libstagefright_bufferqueue_helper-v35.so')
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v34.so')
        .replace_needed('libcodec2_hidl@1.1.so', 'libcodec2_hidl@1.1-v34.so')
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v34.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v34.so')
        .replace_needed('libui.so', 'libui-v34.so'),
    ('vendor/lib64/libcodec2_hidl_plugin-v34.so',
     'vendor/lib64/libsfplugin_ccodec_utils-v34.so'): blob_fixup()
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v34.so'),
    ('vendor/lib64/libcodec2_mtk_c2store.so',
     'vendor/lib64/libcodec2_mtk_vdec.so',
     'vendor/lib64/libcodec2_mtk_venc.so',
     'vendor/lib64/libcodec2_vpp_fa_plugin.so',
     'vendor/lib64/libcodec2_vpp_mi_plugin.so',
     'vendor/lib64/libcodec2_vpp_qt_plugin.so',
     'vendor/lib64/libcodec2_vpp_rs_plugin.so'): blob_fixup()
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v34.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v34.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v34.so')
        .replace_needed('libui.so', 'libui-v34.so'),
    'vendor/lib64/libcodec2_soft_common-v34.so': blob_fixup()
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v34.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v34.so')
        .replace_needed('libui.so', 'libui-v34.so'),
    ('vendor/lib64/libcodec2_vpp_AIMEMC_plugin.so',
     'vendor/lib64/libcodec2_vpp_AISR_plugin.so'): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V4-ndk.so', 'android.hardware.graphics.common-V7-ndk.so')
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v34.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v34.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v34.so'),
    'vendor/lib64/libcodec2_vndk-v34.so': blob_fixup()
        .replace_needed('libui.so', 'libui-v34.so')
        .replace_needed('android.hardware.media.bufferpool2-V1-ndk.so', 'android.hardware.media.bufferpool2-V2-ndk.so'),
    ('vendor/bin/hw/android.hardware.security.keymint-service.strongbox-thales',
     'vendor/bin/hw/android.hardware.security.keymint@3.0-service.trustonic',
     'vendor/bin/moto_eSE_tool',
     'vendor/lib64/libjc_keymint-thales.so',
     'vendor/lib64/libtpa.so'): blob_fixup()
        .replace_needed('lib_android_keymaster_keymint_utils.so', 'lib_android_keymaster_keymint_utils-v34.so')
        .replace_needed('libcppbor_external.so', 'libcppbor_external-v34.so')
        .replace_needed('libkeymint.so', 'libkeymint-v34.so'),
    'vendor/lib64/libkeymint-v34.so': blob_fixup()
        .replace_needed('lib_android_keymaster_keymint_utils.so', 'lib_android_keymaster_keymint_utils-v34.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'SX3',
    'sharp',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
