{{/*
Validate and Get API Key
*/}}
{{- define "servarr.apiKey" -}}
{{- $apiKey := .Values.global.apikey | default "" -}}
{{- if or (lt (len $apiKey) 20) (gt (len $apiKey) 32) -}}
{{- fail (printf "API Key must be between 20 and 32 characters long, got %d characters" (len $apiKey)) -}}
{{- end -}}
{{- if not (regexMatch "^[a-fA-F0-9]+$" $apiKey) -}}
{{- fail "API Key must be a hexadecimal string" -}}
{{- end -}}
{{- $apiKey -}}
{{- end -}}

{{/*
Expand the name of the chart.
*/}}
{{- define "servarr.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "servarr.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "servarr.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "servarr.labels" -}}
helm.sh/chart: {{ include "servarr.chart" . }}
{{ include "servarr.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- with .Values.global.labels }}
{{ toYaml . }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "servarr.selectorLabels" -}}
app.kubernetes.io/name: {{ include "servarr.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Common annotations
*/}}
{{- define "servarr.annotations" -}}
{{- with .Values.global.annotations }}
{{ toYaml . }}
{{- end }}
{{- end }}
