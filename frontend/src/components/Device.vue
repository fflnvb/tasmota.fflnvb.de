<script setup>
import { ref, computed } from 'vue'
const props = defineProps({
    device: {
        type: Object,
        required: true
    }
})

const cleanVersion = computed(() => {
    return props.device.StatusFWR.Version.replace('(tasmota)', '')
})

const wifiRate = computed(() => {
    let signal = Math.abs(props.device.StatusSTS.Wifi.Signal)
    let out
    if (signal <= import.meta.env.VITE_WIFI_MEDIUM || 60) {
        out = {
            icon: "bi-wifi",
            class: "text-bg-success",
        }
    } else if (signal <= import.meta.env.VITE_WIFI_BAD || 90){
        out = {
            icon: "bi-wifi-2",
            class: "text-bg-warning"
        }
    } else {
        out = {
            icon: "bi-wifi-1",
            class: "text-bg-danger"
        }
    }
    return out
})
</script>

<template>
    <div class="row">
        <div class="col-6">
            <small>{{ device.Status.DeviceName }}</small>
            <a :href="'http://' + device.StatusNET.IPAddress" target="_blank" class="ms-1">
                <span class="badge text-bg-secondary">
                    {{ device.StatusNET.IPAddress }} <i class="bi bi-box-arrow-in-up-right"></i>
                </span>
            </a>
            
        </div>
        <div class="col-2">
            <small>{{ device.Status.Topic }}</small>
        </div>
        <div class="col-2">
            <span class="badge me-1" :class="wifiRate.class">
                <i class="bi" :class="wifiRate.icon"></i> {{ device.StatusSTS.Wifi.Signal }} dBm
            </span>
        </div>
        <div class="col-2">
            {{ cleanVersion }}
            <a :href="'http://' + device.StatusNET.IPAddress + '/u1'" role="button" class="btn btn-outline-secondary btn-sm"
            target="_blank" onclick="return confirm('Are you sure?')"><i class="bi bi-arrow-up-circle"></i></a></div>
    </div>


</template>

<style scoped>

</style>
