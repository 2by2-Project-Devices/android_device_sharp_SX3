#
# SPDX-FileCopyrightText: LineageOS
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device makefile.
$(call inherit-product, device/sharp/SX3/device.mk)

# Inherit some common lineageOS stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# WitAqua stuff
PROCESSOR_INFO := MediaTek Dimensity 700
WITAQUA_MAINTAINER := kailua

TARGET_BOOT_ANIMATION_RES := 1080

PRODUCT_NAME := lineage_SX3
PRODUCT_DEVICE := SX3
PRODUCT_MANUFACTURER := sharp
PRODUCT_BRAND := SHARP
PRODUCT_MODEL := SX3

PRODUCT_GMS_CLIENTID_BASE := android-sharp

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="SX3_00WW_FIH-user 15 AP3A.240905.015.A2 p1rck6991v164P11 release-keys" \
    BuildFingerprint=SHARP/SX3_00WW/SX3:15/AP3A.240905.015.A2/00WW_3_330:user/release-keys
