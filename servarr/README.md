# servarr



![Version: 0.22.7](https://img.shields.io/badge/Version-0.22.7-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 0.22.7](https://img.shields.io/badge/AppVersion-0.22.7-informational?style=flat-square) 

Servarr complete Helm Chart for Kubernetes

**Homepage:** <https://github.com/datahub-local/servarr>

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| alvsanand | <alvsanand@gmail.com> |  |

## Source Code

* <https://github.com/datahub-local/servarr>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://oci.trueforge.org/truecharts | bazarr | 23.2.15 |
| oci://oci.trueforge.org/truecharts | flaresolverr | 16.14.14 |
| oci://oci.trueforge.org/truecharts | jellyfin | 22.2.25 |
| oci://oci.trueforge.org/truecharts | jellyseerr | 13.13.17 |
| oci://oci.trueforge.org/truecharts | prowlarr | 21.3.16 |
| oci://oci.trueforge.org/truecharts | qbittorrent | 24.2.16 |
| oci://oci.trueforge.org/truecharts | radarr | 26.3.15 |
| oci://oci.trueforge.org/truecharts | sonarr | 25.2.15 |

---

> [!IMPORTANT]  
> Please consider that this chart is a collection of several public helm charts.
> These are included as sub-charts of the Servarr chart and, due to some Helm limitation, some configuration are only possible via values file.
> For this reason, the servarr default [values.yaml](#./values.yaml) included in the chart is quite huge and it used to model the configuration of the subcharts.
> But don't you worry! I provided some handy values, using [yaml anchors](https://medium.com/@kinghuang/docker-compose-anchors-aliases-extensions-a1e4105d70bd), to defined top-level fields.
> Follow the table below and forget everything else. 

> [!CAUTION] 
> Please, do not remove Anchors when you see them (the strage syntax with the `&`) and make sure you include all the parameters that are using the anchors. Check the minimal `values.yaml` reference.

<details><summary>Minimal <code>values.yaml</code> sample</summary>

```yaml
global:
  apikey: &apikey "<replace-with-an-api-key>"
  storageClassName: &storageClassName "<replace-with-your-storage-class-name>"
  ingressClassName: &ingressClassName "<replace-with-your-ingress-class-name>"
  certManagerClusterIssuer: &issuer

metrics:
  enabled: &metricsEnabled false

dash:
  username:
  password:
  mail:
  countryCode: "US"
  preferredLanguage: "en"

torrent:
  username:
  password:

volumes:
  storageClass: *storageClassName
  downloads:
    name: &downloads-volume downloads-volume
    size: 100Gi
  media:
    name: &media-volume media-volume
    size: 250Gi
  torrentConfig:
    name: &torrentConfig torrent-config
    size: 250Mi

sonarr:
  metrics:
    main:
      enabled: *metricsEnabled
  workload:
    main:
      podSpec:
        containers:
          main:
            env:
              SONARR__AUTH__APIKEY: *apikey
          exportarr:
            env:
              API_KEY: *apikey
  ingress:
    sonarr-ing:
      annotations:
        cert-manager.io/cluster-issuer: *issuer
      ingressClassName: *ingressClassName
      hosts:
        - host: sonarr.local
          paths:
            - path: /
              pathType: Prefix
      tls:
        - hosts:
            - sonarr.local
          secretName: sonarr-tls
  persistence:
    config:
      storageClass: *storageClassName
    media:
      existingClaim: *media-volume
    downloads:
      existingClaim: *downloads-volume

radarr:
  metrics:
    main:
      enabled: *metricsEnabled
  workload:
    main:
      podSpec:
        containers:
          main:
            env:
              RADARR__AUTH__APIKEY: *apikey
          exportarr:
            env:
              API_KEY: *apikey
  ingress:
    radarr-ing:
      annotations:
        cert-manager.io/cluster-issuer: *issuer
      ingressClassName: *ingressClassName
      hosts:
        - host: radarr.local
          paths:
            - path: /
              pathType: Prefix
      tls:
        - hosts:
            - radarr.local
          secretName: radarr-tls
  persistence:
    config:
      storageClass: *storageClassName
    media:
      existingClaim: *media-volume
    downloads:
      existingClaim: *downloads-volume

jellyfin:
  metrics:
    main:
      enabled: *metricsEnabled
  ingress:
    jellyfin-ing:
      annotations:
        cert-manager.io/cluster-issuer: *issuer
      ingressClassName: *ingressClassName
      hosts:
        - host: jellyfin.local
          paths:
            - path: /
              pathType: Prefix
      tls:
        - hosts:
            - jellyfin.local
          secretName: jellyfin-tls
  persistence:
    config:
      storageClass: *storageClassName
    media:
      existingClaim: *media-volume

jellyseerr:
  metrics:
    main:
      enabled: *metricsEnabled
  ingress:
    jellyseerr-ing:
      annotations:
        cert-manager.io/cluster-issuer: *issuer
      ingressClassName: *ingressClassName
      hosts:
        - host: jellyseerr.local
          paths:
            - path: /
              pathType: Prefix
      tls:
        - hosts:
            - jellyseerr.local
          secretName: jellyseerr-tls
  persistence:
    config:
      storageClass: *storageClassName
    media:
      existingClaim: *media-volume

qbittorrent:
  metrics:
    main:
      enabled: *metricsEnabled
  ingress:
    qbittorrent-ing:
      annotations:
        cert-manager.io/cluster-issuer: *issuer
      ingressClassName: *ingressClassName
      hosts:
        - host: torrent.local
          paths:
            - path: /
              pathType: Prefix
      tls:
        - hosts:
            - torrent.local
          secretName: torrent-tls
  persistence:
    config:
      existingClaim: *torrentConfig
    downloads:
      existingClaim: *downloads-volume

prowlarr:
  metrics:
    main:
      enabled: *metricsEnabled
  workload:
    main:
      podSpec:
        containers:
          main:
            env:
              PROWLARR__AUTH__APIKEY: *apikey
          exportarr:
            env:
              API_KEY: *apikey
  ingress:
    prowlarr-ing:
      annotations:
        cert-manager.io/cluster-issuer: *issuer
      ingressClassName: *ingressClassName
      hosts:
        - host: prowlarr.local
          paths:
            - path: /
              pathType: Prefix
      tls:
        - hosts:
            - prowlarr.local
          secretName: prowlarr-tls
  persistence:
    config:
      storageClass: *storageClassName

flaresolverr:
  metrics:
    main:
      enabled: *metricsEnabled
  persistence:
    config:
      storageClass: *storageClassName
```

</details>

---

## Values

### Jellyfin

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| dash.countryCode | string | US | Insert the Jellyfin country code |
| dash.mail | string | No default value | Insert Jellyfin login mail (will be used also for Jellyseerr integration) |
| dash.password | string | No default value | Insert Jellyfin password (will be used also for Jellyseerr) |
| dash.preferredLanguage | string | en | Insert the Jellyfin preferred language |
| dash.username | string | No default value | Insert the Jellyfin username (will be used also for Jellyseerr) |

### Bazarr

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| dash.preferredSubtitlesLanguages | string | en,es | Insert the Bazarr preferred subtitles languages (comma separated) |
| dash.preferredSubtitlesProviders | string | No default value. Example: "opensubtitlescom" | Insert the Bazarr preferred subtitles providers (comma separated) |
| dash.preferredSubtitlesProvidersSettings | string | No default value | Insert the Bazarr preferred subtitles providers settings (comma separated). Example: "opensubtitlescom-username=some_username,opensubtitlescom-password=some_password,opensubtitlescom-include_ai_translated=true" |

### Global

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.apikey | string | It is obligatory to set this value | Insert your Prowlarr, Sonarr, Radarr API key here (one to rule them all!). Must be 20 to 32 hexadecimal characters. |
| global.authRequired | bool | DisabledForLocalAddresses | This tag will set the auth required. Valid values are  "DisabledForLocalAddresses" | "Enabled" |
| global.certManagerClusterIssuer | string | No default value, leave empty if not required | Insert your cert manager cluster issuer, e.g.: letsencrypt-cloudflare. Do not remove the `&issuer` anchor! |
| global.ingressClassName | string | nginx | Insert your ingress class here, e.g.: &ingressClassName nginx. Do not remove the `&ingressCassName` anchor, and do not leave the anchor value empty, otherwise you will face a `null` value error! |
| global.ingressHostPattern | string | https://SERVICE.local | User a hostname pattern to use in the ingress instead of overriding each service, e.g.: "SERVICE.local". "SERVICE" should be included and it will be replace by the lowercase name of the service. |
| global.storageClassName | string | `"network-block"` | Insert your storage class here, e.g.: &storageClassName network-block. Do not remove the `&storageClassName` anchor! |

### Prowlarr

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| indexers | list | The body of the 1337x index is provided as default | The indexers list. Each element of the list is the yaml-formatted body of the [Prowlarr API request](https://prowlarr.com/docs/api/#/Indexer/post_api_v1_indexer) to add that index. |

### Metrics

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| metrics.enabled | bool | `false` | Anchor to set wether to deploy the export sidecar pods or not. Requires the Prometheus stack. Do not remove the `&metricsEnabled` anchor! |

### Jellyseerr

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| notifications.telegram.bot_apitoken | string | No default value | Insert your Telegram Bot API token |
| notifications.telegram.chat_id | string | No default value | Insert the Telegram Chat id, check @get_id_bot for this |
| notifications.telegram.enabled | bool | `true` | Enable the Telegram notifications |

### Torrent

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| qbittorrent.csrf_protection | bool | false | Whether to enable or disable CSRF Protection on qBitTorrent WebGUI |
| torrent.password | string | No default value | password of the qBitTorrent admin user. Must be at least of 8 characters. |
| torrent.username | string | No default value | username of the qBitTorrent admin user |

### Tags

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| tags.movies | bool | true | This tag will deploy: Radarr, Prowlarr, QBitTorrent, Jellyseerr, Jellyfin, Flaresolverr, Bazarr |
| tags.music | bool | true | This tag will deploy: Prowlarr, QBitTorrent, Jellyfin, Flaresolverr |
| tags.tvseries | bool | true | This tag will deploy: Sonarr, Prowlarr, QBitTorrent, Jellyseerr, Jellyfin, Flaresolverr, Bazarr |

### Storage

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| volumes.downloads | object | See the sub fields | configuration of the volume used for torrent downloads |
| volumes.downloads.name | string | `"downloads-volume"` | Name of the download pvc. Do not remove the `&downloads-volume` anchor! |
| volumes.downloads.size | string | `"100Gi"` | Size of the downloads volume, in Kubernets format |
| volumes.initConfig | object | See the sub fields | configuration of the volume used for init scripts state |
| volumes.initConfig.name | string | `"init-config"` | Name of the init configuration pvc. Do not remove the `&initConfig` anchor! |
| volumes.initConfig.size | string | `"10Mi"` | Size of the init configuration volume, in Kubernets format |
| volumes.media | object | See the sub fields | configuration of the volume used for media storage (i.e.: where movies and tv shows file will be permanently stored) |
| volumes.media.name | string | `"media-volume"` | Name of the media pvc. Do not remove the `&media-volume` anchor! |
| volumes.media.size | string | `"250Gi"` | Size of the media volume, in Kubernets format |
| volumes.torrentConfig | object | See the sub fields | configuration of the volume used for qBitTorrent internal configuration |
| volumes.torrentConfig.name | string | `"torrent-config"` | Name of the torrent configuration pvc. Do not remove the `&torrentConfig` anchor! |
| volumes.torrentConfig.size | string | `"250Mi"` | Size of the torrent configuration volume, in Kubernets format |

### Other Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| argoCD | bool | false | The flag changes the behavior id deployed with ArgoCD. |
| bazarr | object | `{}` |  |
| extraResources | list | `[]` | Extra resources to deploy |
| flaresolverr.workload.main.podSpec.containers.main.probes.liveness.path | string | `"/health"` |  |
| flaresolverr.workload.main.podSpec.containers.main.probes.readiness.path | string | `"/health"` |  |
| flaresolverr.workload.main.podSpec.containers.main.probes.startup.path | string | `"/health"` |  |
| global.annotations | object | `{}` |  |
| global.authMethod | string | `nil` |  |
| global.labels | object | `{}` |  |
| init.annotations | object | `{}` |  |
| init.image.pullPolicy | string | `"IfNotPresent"` |  |
| init.image.repository | string | `"python"` |  |
| init.image.tag | float | `3.14` |  |
| init.job.activeDeadlineSeconds | int | 300 | The duration in seconds relative to the StartTime that the job may be continuously active before the system tries to terminate it; value must be positive integer |
| init.job.backoffLimit | int | 1 | The number of retries before considering a Job as failed |
| init.nodeSelector | object | `{}` |  |
| init.resources.limits.cpu | string | `"100m"` |  |
| init.resources.limits.memory | string | `"128Mi"` |  |
| init.resources.requests.cpu | string | `"100m"` |  |
| init.resources.requests.memory | string | `"128Mi"` |  |
| init.tolerations | list | `[]` |  |
| init.waitFor.image.pullPolicy | string | `"IfNotPresent"` |  |
| init.waitFor.image.repository | string | `"busybox"` |  |
| init.waitFor.image.tag | string | `"stable"` |  |
| init.waitFor.resources.limits.cpu | string | `"50m"` |  |
| init.waitFor.resources.limits.memory | string | `"64Mi"` |  |
| init.waitFor.resources.requests.cpu | string | `"10m"` |  |
| init.waitFor.resources.requests.memory | string | `"32Mi"` |  |
| jellyfin.chartContext.appUrl | string | `"https://{{ replace \"SERVICE\" \"jellyfin\" .Values.global.ingressHostPattern }}"` |  |
| jellyseerr | object | `{}` |  |
| prowlarr | object | `{}` |  |
| qbittorrent.addons.gluetun.enabled | bool | `false` |  |
| radarr | object | `{}` |  |
| sonarr | object | `{}` |  |


----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.14.2](https://github.com/norwoodj/helm-docs/releases/v1.14.2)
