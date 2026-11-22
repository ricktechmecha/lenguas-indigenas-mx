# Cobertura mundial de lenguas — matriz honesta

> Generado por `tools/build_coverage_matrix.py` — no editar a mano.

## Resumen

| Tier | Significado | Conteo |
|---|---|---|
| 🟢 **A** | Voz MMS + traducción NMT dedicada (Google) | **116** |
| 🟡 **B** | Voz MMS, traducción solo LLM (baja calidad en bajos recursos) | **901** |
| 🔵 **C** | Solo texto (sin checkpoint MMS) | **3** |
| 🔴 **D** | Sin datos en el registro (resto de ISO 639-3) | **~6880** |

> ⚠️ **Honestidad:** 'voz MMS' ≠ traducción buena. En tier B el LLM suele fallar o inventar (medido: zapoteco ≈ 0.01 en back-translation). Ninguna traducción está validada por hablante nativo.


## 🟢 Tier A — cobertura completa (voz + traducción) — 116 lenguas

Traducción por NMT dedicado de Google Translate. Las de la tabla MX son las de mayor calidad relativa.

| ISO | Lengua | Región | Familia | Orden | Google |
|---|---|---|---|---|---|
| `ayr` | Aymara (Central) | Américas | Aymaran | SOV | ay |
| `hat` | Haitian Creole | Américas | other | — | ht |
| `jam` | Jamaican Creole | Américas | other | — | jam |
| `kek` | K'ekchí | Américas | Mayan | — | kek |
| `mam` | Mam | Américas | Mayan | VSO | mam |
| `pap` | Papiamentu | Américas | other | — | pap |
| `quz` | Quechua (Cuzco) | Américas | Quechuan | — | qu |
| `yua` | Yucatec | Américas | Mayan | — | yua |
| `zai` | Zapotec (Isthmus) | Américas | Oto-Manguean | VSO | zap |
| `ace` | Acehnese | Eurasia | Austronesian | No dominant order | ace |
| `asm` | Assamese | Eurasia | Indo-European | SOV | as |
| `awa` | Awadhi | Eurasia | Indo-European | — | awa |
| `bak` | Bashkir | Eurasia | Altaic | — | ba |
| `ben` | Bengali | Eurasia | Indo-European | SOV | bn |
| `bul` | Bulgarian | Eurasia | Indo-European | SVO | bg |
| `mya` | Burmese | Eurasia | Sino-Tibetan | SOV | my |
| `cat` | Catalan | Eurasia | Indo-European | SVO | ca |
| `nld` | Dutch | Eurasia | Indo-European | No dominant order | nl |
| `eng` | English | Eurasia | Indo-European | SVO | en |
| `fin` | Finnish | Eurasia | Uralic | SVO | fi |
| `fra` | French | Eurasia | Indo-European | SVO | fr |
| `deu` | German (Timisoara) | Eurasia | Indo-European | — | de |
| `ell` | Greek (Modern) | Eurasia | Indo-European | No dominant order | el |
| `guj` | Gujarati | Eurasia | Indo-European | SOV | gu |
| `heb` | Hebrew (Modern) | Eurasia | Afro-Asiatic | SVO | iw |
| `hin` | Hindi | Eurasia | Indo-European | SOV | hi |
| `hun` | Hungarian | Eurasia | Uralic | No dominant order | hu |
| `isl` | Icelandic | Eurasia | Indo-European | SVO | is |
| `kac` | Jingpho | Eurasia | Sino-Tibetan | SOV | kac |
| `kan` | Kannada | Eurasia | Dravidian | SOV | kn |
| `kaz` | Kazakh | Eurasia | Altaic | — | kk |
| `khm` | Khmer | Eurasia | Austro-Asiatic | SVO | km |
| `kir` | Kirghiz | Eurasia | Altaic | — | ky |
| `kor` | Korean | Eurasia | Korean | SOV | ko |
| `lao` | Lao | Eurasia | Tai-Kadai | SVO | lo |
| `lav` | Latvian | Eurasia | Indo-European | SVO | lv |
| `mai` | Maithili | Eurasia | Indo-European | — | mai |
| `zlm` | Malay (Kuala Lumpur) | Eurasia | Austronesian | — | ms |
| `mal` | Malayalam | Eurasia | Dravidian | SOV | ml |
| `mar` | Marathi | Eurasia | Indo-European | SOV | mr |
| `new` | Newar (Dolakha) | Eurasia | Sino-Tibetan | SOV | new |
| `ory` | Oriya | Eurasia | Indo-European | SOV | or |
| `pan` | Panjabi | Eurasia | Indo-European | SOV | pa |
| `pol` | Polish | Eurasia | Indo-European | SVO | pl |
| `por` | Portuguese | Eurasia | Indo-European | SVO | pt |
| `ron` | Romanian | Eurasia | Indo-European | SVO | ro |
| `rus` | Russian | Eurasia | Indo-European | SVO | ru |
| `shn` | Shan | Eurasia | Tai-Kadai | SVO | shn |
| `spa` | Spanish (Canary Islands) | Eurasia | Indo-European | — | es |
| `swe` | Swedish (Västerbotten) | Eurasia | Indo-European | — | sv |
| `tgk` | Tajik | Eurasia | Indo-European | SOV | tg |
| `tam` | Tamil (Spoken) | Eurasia | Dravidian | — | ta |
| `tat` | Tatar | Eurasia | Altaic | SOV | tt |
| `tel` | Telugu | Eurasia | Dravidian | SOV | te |
| `tha` | Thai | Eurasia | Tai-Kadai | SVO | th |
| `bod` | Tibetan (Modern Literary) | Eurasia | Sino-Tibetan | SOV | bo |
| `tur` | Turkish | Eurasia | Altaic | SOV | tr |
| `udm` | Udmurt | Eurasia | Uralic | SOV | udm |
| `ukr` | Ukrainian | Eurasia | Indo-European | SVO | uk |
| `vie` | Vietnamese | Eurasia | Austro-Asiatic | SVO | vi |
| `cym` | Welsh | Eurasia | Indo-European | VSO | cy |
| `sah` | Yakut | Eurasia | Altaic | SOV | sah |
| `ban` | Balinese | Papúa y Oceanía | Austronesian | — | ban |
| `btx` | Batak (Karo) | Papúa y Oceanía | Austronesian | No dominant order | btx |
| `bbc` | Batak (Toba) | Papúa y Oceanía | Austronesian | VOS | bbc |
| `fij` | Fijian | Papúa y Oceanía | Austronesian | No dominant order | fj |
| `hil` | Hiligaynon | Papúa y Oceanía | Austronesian | VSO | hil |
| `iba` | Iban | Papúa y Oceanía | Austronesian | SVO | iba |
| `ilo` | Ilocano | Papúa y Oceanía | Austronesian | VSO | ilo |
| `ind` | Indonesian (Jakarta) | Papúa y Oceanía | Austronesian | — | id |
| `jav` | Javanese | Papúa y Oceanía | Austronesian | — | jw |
| `pam` | Kapampangan | Papúa y Oceanía | Austronesian | — | pam |
| `mak` | Makassar | Papúa y Oceanía | Austronesian | — | mak |
| `min` | Minangkabau | Papúa y Oceanía | Austronesian | No dominant order | min |
| `pag` | Pangasinan | Papúa y Oceanía | Austronesian | VSO | pag |
| `smo` | Samoan | Papúa y Oceanía | Austronesian | No dominant order | sm |
| `sun` | Sundanese | Papúa y Oceanía | Austronesian | SVO | su |
| `tgl` | Tagalog | Papúa y Oceanía | Austronesian | VSO | tl |
| `tpi` | Tok Pisin | Papúa y Oceanía | other | — | tpi |
| `war` | Waray-Waray | Papúa y Oceanía | Austronesian | — | war |
| `ach` | Acholi | África | Eastern Sudanic | SVO | ach |
| `aka` | Akan | África | Niger-Congo | SVO | ak |
| `amh` | Amharic | África | Afro-Asiatic | SOV | am |
| `bam` | Bambara | África | Mande | SOV | bm |
| `bem` | Bemba | África | Niger-Congo | — | bem |
| `nya` | Chichewa | África | Niger-Congo | SVO | ny |
| `dyu` | Dyula | África | Mande | — | dyu |
| `ewe` | Ewe | África | Niger-Congo | SVO | ee |
| `fon` | Fongbe | África | Niger-Congo | SVO | fon |
| `hau` | Hausa | África | Afro-Asiatic | SVO | ha |
| `kin` | Kinyarwanda | África | Niger-Congo | SVO | rw |
| `mfe` | Mauritian Creole | África | other | — | mfe |
| `nus` | Nuer | África | Eastern Sudanic | No dominant order | nus |
| `sna` | Shona | África | Niger-Congo | SVO | sn |
| `som` | Somali | África | Afro-Asiatic | SOV | so |
| `sus` | Susu | África | Mande | SOV | sus |
| `swh` | Swahili | África | Niger-Congo | SVO | sw |
| `tir` | Tigrinya | África | Afro-Asiatic | SOV | ti |
| `yor` | Yoruba | África | Niger-Congo | SVO | yo |
| `nah-hua` | Náhuatl de la Huasteca | — | — | — | nhe |
| `nhe` | Náhuatl de la Huasteca | — | — | — | nhe |
| `zap` | Zapoteco del Istmo | — | — | — | zap |
| `alz` | — | — | — | — | alz |
| `ara` | — | — | — | — | ar |
| `azj-script_latin` | — | — | — | — | az |
| `bts` | — | — | — | — | bts |
| `fas` | — | — | — | — | fa |
| `grn` | — | — | — | — | gn |
| `kri` | — | — | — | — | kri |
| `mam-dialect_central` | — | — | — | — | mam |
| `mam-dialect_northern` | — | — | — | — | mam |
| `mam-dialect_southern` | — | — | — | — | mam |
| `mam-dialect_western` | — | — | — | — | mam |
| `orm` | — | — | — | — | om |
| `uig-script_arabic` | — | — | — | — | ug |
| `urd-script_arabic` | — | — | — | — | ur |


## 🟡 Tier B — voz disponible, traducción débil — 901 lenguas

MMS-TTS existe pero NO hay par Google verificado: la traducción depende del LLM (Groq/local). Revisar caso por caso; algunas (var. regionales) pueden usar el par de la lengua vecina con precaución.

| ISO | Lengua | Región | Familia | Orden | Google |
|---|---|---|---|---|---|
| `aca` | Achagua | Américas | Arawakan | SVO | — |
| `acu` | Achuar | Américas | Jivaroan | — | — |
| `guq` | Aché | Américas | Tupian | — | — |
| `acr` | Achí | Américas | Mayan | — | — |
| `agu` | Aguacatec | Américas | Mayan | — | — |
| `agr` | Aguaruna | Américas | Jivaroan | — | — |
| `ake` | Akawaio | Américas | Cariban | — | — |
| `ame` | Amuesha | Américas | Arawakan | — | — |
| `arl` | Arabela | Américas | Zaparoan | — | — |
| `kwi` | Awa Pit | Américas | Barbacoan | SOV | — |
| `ayo` | Ayoreo | Américas | Zamucoan | SVO | — |
| `boa` | Bora | Américas | Boran | — | — |
| `bor` | Bororo | Américas | Bororoan | — | — |
| `sab` | Buglere | Américas | Chibchan | — | — |
| `kaq` | Capanahua | Américas | Pano-Tacanan | — | — |
| `car` | Carib | Américas | Cariban | SOV | — |
| `cya` | Chatino (Nopala) | Américas | Oto-Manguean | — | — |
| `cap` | Chipaya | Américas | Uru-Chipaya | SOV | — |
| `caa` | Chortí | Américas | Mayan | — | — |
| `kog` | Cogui | Américas | Chibchan | — | — |
| `des` | Desano | Américas | Tucanoan | SOV | — |
| `emp` | Emberá (Northern) | Américas | Choco | — | — |
| `sja` | Epena Pedee | Américas | Choco | SOV | — |
| `ese` | Ese Ejja | Américas | Pano-Tacanan | SOV | — |
| `cab` | Garífuna | Américas | Arawakan | VSO | — |
| `guc` | Goajiro | Américas | Arawakan | VSO | — |
| `guh` | Guahibo | Américas | Guahiban | SOV | — |
| `gub` | Guajajara | Américas | Tupian | VSO | — |
| `gum` | Guambiano | Américas | Barbacoan | — | — |
| `gvc` | Guanano | Américas | Tucanoan | — | — |
| `guo` | Guayabero | Américas | Guahiban | — | — |
| `hwc` | Hawaiian Creole | Américas | other | — | — |
| `hub` | Huambisa | Américas | Jivaroan | — | — |
| `hus` | Huastec | Américas | Mayan | SVO | — |
| `huv` | Huave (San Mateo del Mar) | Américas | Huavean | SVO | — |
| `hto` | Huitoto (Minica) | Américas | Witotoan | SOV | — |
| `huu` | Huitoto (Murui) | Américas | Witotoan | SOV | — |
| `ign` | Ignaciano | Américas | Arawakan | — | — |
| `inb` | Inga | Américas | Quechuan | — | — |
| `jac` | Jakaltek | Américas | Mayan | VSO | — |
| `jiv` | Jivaro | Américas | Jivaroan | SOV | — |
| `kay` | Kamaiurá | Américas | Tupian | SOV | — |
| `kjb` | Kanjobal (Eastern) | Américas | Mayan | — | — |
| `knj` | Kanjobal (Western) | Américas | Mayan | — | — |
| `kyz` | Kayabí | Américas | Tupian | SOV | — |
| `kvn` | Kuna | Américas | Chibchan | SOV | — |
| `gwi` | Kutchin | Américas | Na-Dene | — | — |
| `lac` | Lacandón | Américas | Mayan | No dominant order | — |
| `enx` | Lengua | Américas | Mascoian | — | — |
| `mca` | Maca | Américas | Matacoan | — | — |
| `mcb` | Machiguenga | Américas | Arawakan | — | — |
| `myy` | Macuna | Américas | Tucanoan | — | — |
| `mbc` | Macushi | Américas | Cariban | No dominant order | — |
| `mfy` | Mayo | Américas | Uto-Aztecan | — | — |
| `maz` | Mazahua | Américas | Oto-Manguean | — | — |
| `maq` | Mazatec (Chiquihuitlán) | Américas | Oto-Manguean | — | — |
| `mco` | Mixe (Coatlán) | Américas | Mixe-Zoque | — | — |
| `mim` | Mixtec (Alacatlatzala) | Américas | Oto-Manguean | — | — |
| `mib` | Mixtec (Atatlahuca) | Américas | Oto-Manguean | — | — |
| `mih` | Mixtec (Chayuco) | Américas | Oto-Manguean | — | — |
| `mie` | Mixtec (Ocotepec) | Américas | Oto-Manguean | VSO | — |
| `mil` | Mixtec (Peñoles) | Américas | Oto-Manguean | VSO | — |
| `cas` | Mosetén | Américas | Mosetenan | SVO | — |
| `bmr` | Muinane | Américas | Boran | — | — |
| `mbj` | Nadëb | Américas | Nadahup | OSV | — |
| `ncj` | Nahuatl (Huauchinango) | Américas | Uto-Aztecan | — | — |
| `nhx` | Nahuatl (Mecayapan Isthmus) | Américas | Uto-Aztecan | — | — |
| `ncl` | Nahuatl (Michoacán) | Américas | Uto-Aztecan | SVO | — |
| `azz` | Nahuatl (Sierra de Zacapoaxtla) | Américas | Uto-Aztecan | — | — |
| `ngu` | Nahuatl (Xalitla) | Américas | Uto-Aztecan | — | — |
| `nab` | Nambikuára (Southern) | Américas | Nambikuaran | SOV | — |
| `djk` | Ndyuka | Américas | other | SVO | — |
| `gym` | Ngäbere | Américas | Chibchan | SOV | — |
| `not` | Nomatsiguenga | Américas | Arawakan | — | — |
| `ood` | O'odham | Américas | Uto-Aztecan | No dominant order | — |
| `ote` | Otomí (Mezquital) | Américas | Oto-Manguean | VOS | — |
| `otq` | Otomí (Santiago Mexquititlan) | Américas | Oto-Manguean | — | — |
| `pao` | Paiute (Northern) | Américas | Uto-Aztecan | SOV | — |
| `pab` | Paresi | Américas | Arawakan | — | — |
| `pad` | Paumarí | Américas | Arauan | SVO | — |
| `pir` | Piratapuyo | Américas | Tucanoan | — | — |
| `pib` | Piro | Américas | Arawakan | SOV | — |
| `poi` | Popoluca (Sierra) | Américas | Mixe-Zoque | SVO | — |
| `pui` | Puinave | Américas | Puinave | — | — |
| `tsz` | Purépecha | Américas | Tarascan | SVO | — |
| `pbb` | Páez | Américas | Páezan | SOV | — |
| `quy` | Quechua (Ayacucho) | Américas | Quechuan | — | — |
| `qvc` | Quechua (Cajamarca) | Américas | Quechuan | — | — |
| `quh` | Quechua (Cochabamba) | Américas | Quechuan | — | — |
| `qub` | Quechua (Huallaga) | Américas | Quechuan | SOV | — |
| `qvn` | Quechua (Tarma) | Américas | Quechuan | — | — |
| `xsu` | Sanuma | Américas | Yanomam | SOV | — |
| `srm` | Saramaccan | Américas | other | — | — |
| `sey` | Secoya | Américas | Tucanoan | — | — |
| `mcd` | Sharanahua | Américas | Pano-Tacanan | SOV | — |
| `shp` | Shipibo-Konibo | Américas | Pano-Tacanan | SOV | — |
| `snn` | Siona | Américas | Tucanoan | — | — |
| `sri` | Siriano | Américas | Tucanoan | — | — |
| `srn` | Sranan | Américas | other | — | — |
| `tna` | Tacana | Américas | Pano-Tacanan | No dominant order | — |
| `tac` | Tarahumara (Western) | Américas | Uto-Aztecan | SOV | — |
| `tav` | Tatuyo | Américas | Tucanoan | — | — |
| `ttc` | Tectiteco | Américas | Mayan | — | — |
| `tee` | Tepehua (Huehuetla) | Américas | Totonacan | No dominant order | — |
| `tpt` | Tepehua (Tlachichilco) | Américas | Totonacan | SVO | — |
| `stp` | Tepehuan (Southeastern) | Américas | Uto-Aztecan | — | — |
| `tfr` | Teribe | Américas | Chibchan | SOV | — |
| `ter` | Terêna | Américas | Arawakan | — | — |
| `tew` | Tewa (San Juan Pueblo) | Américas | Kiowa-Tanoan | — | — |
| `tca` | Ticuna | Américas | Ticuna | No dominant order | — |
| `tri` | Tiriyo | Américas | Cariban | OVS | — |
| `tob` | Toba | Américas | Guaicuruan | No dominant order | — |
| `jic` | Tol | Américas | Tol | — | — |
| `tos` | Totonac (Sierra) | Américas | Totonacan | — | — |
| `trs` | Trique (Chicahuaxtla) | Américas | Oto-Manguean | — | — |
| `trc` | Trique (Copala) | Américas | Oto-Manguean | VSO | — |
| `tuf` | Tunebo | Américas | Chibchan | — | — |
| `tue` | Tuyuca | Américas | Tucanoan | SOV | — |
| `ura` | Urarina | Américas | Urarina | OVS | — |
| `urb` | Urubú-Kaapor | Américas | Tupian | SOV | — |
| `waw` | Wai Wai | Américas | Cariban | No dominant order | — |
| `bao` | Waimaha | Américas | Tucanoan | — | — |
| `wap` | Wapishana | Américas | Arawakan | — | — |
| `wba` | Warao | Américas | Warao | — | — |
| `noa` | Waunana | Américas | Choco | — | — |
| `way` | Wayana | Américas | Cariban | — | — |
| `xer` | Xerénte | Américas | Macro-Ge | SOV | — |
| `yad` | Yagua | Américas | Peba-Yaguan | No dominant order | — |
| `yaa` | Yaminahua | Américas | Pano-Tacanan | SOV | — |
| `ycn` | Yucuna | Américas | Arawakan | SVO | — |
| `yuz` | Yuracare | Américas | Yuracare | — | — |
| `zaa` | Zapotec (Juárez) | Américas | Oto-Manguean | — | — |
| `zaw` | Zapotec (Mitla) | Américas | Oto-Manguean | VSO | — |
| `zpm` | Zapotec (Mixtepec) | Américas | Oto-Manguean | — | — |
| `zpi` | Zapotec (Quiegolani) | Américas | Oto-Manguean | — | — |
| `zab` | Zapotec (San Lucas Quiaviní) | Américas | Oto-Manguean | — | — |
| `zpz` | Zapotec (Texmelucan) | Américas | Oto-Manguean | — | — |
| `zav` | Zapotec (Yatzachi) | Américas | Oto-Manguean | — | — |
| `zos` | Zoque (Francisco León) | Américas | Mixe-Zoque | — | — |
| `tcs` | Broken | Australia | other | — | — |
| `rop` | Kriol (Ngukurr) | Australia | other | — | — |
| `acn` | Achang | Eurasia | Sino-Tibetan | — | — |
| `agx` | Aghul | Eurasia | Nakh-Daghestanian | — | — |
| `ahk` | Akha | Eurasia | Sino-Tibetan | SOV | — |
| `sqi` | Albanian | Eurasia | Indo-European | SVO | — |
| `alt` | Altai (Southern) | Eurasia | Altaic | — | — |
| `adx` | Amdo (Themchen) | Eurasia | Sino-Tibetan | — | — |
| `hyw` | Armenian (Western) | Eurasia | Indo-European | SOV | — |
| `ava` | Avar | Eurasia | Nakh-Daghestanian | SOV | — |
| `azb` | Azari (Iranian) | Eurasia | Altaic | SOV | — |
| `bgq` | Bagri | Eurasia | Indo-European | — | — |
| `bdq` | Bahnar | Eurasia | Austro-Asiatic | — | — |
| `eus` | Basque | Eurasia | Basque | SOV | — |
| `bgr` | Bawm | Eurasia | Sino-Tibetan | SOV | — |
| `bru` | Bru (Eastern) | Eurasia | Austro-Asiatic | — | — |
| `dar` | Dargwa | Eurasia | Nakh-Daghestanian | SOV | — |
| `dhi` | Dhimal | Eurasia | Sino-Tibetan | SOV | — |
| `div` | Dhivehi | Eurasia | Indo-European | — | — |
| `mhu` | Digaro | Eurasia | Sino-Tibetan | SOV | — |
| `dgo` | Dogri | Eurasia | Indo-European | — | — |
| `fao` | Faroese | Eurasia | Indo-European | — | — |
| `grt` | Garo | Eurasia | Sino-Tibetan | SOV | — |
| `glk` | Gilaki | Eurasia | Indo-European | — | — |
| `hak` | Hakka | Eurasia | Sino-Tibetan | SVO | — |
| `hlb` | Halbi | Eurasia | Indo-European | — | — |
| `hoc` | Ho | Eurasia | Austro-Asiatic | — | — |
| `itl` | Itelmen | Eurasia | Chukotko-Kamchatkan | SOV | — |
| `jun` | Juang | Eurasia | Austro-Asiatic | — | — |
| `krc` | Karachay-Balkar | Eurasia | Altaic | SOV | — |
| `kaa` | Karakalpak | Eurasia | Altaic | SOV | — |
| `krl` | Karelian | Eurasia | Uralic | — | — |
| `xdy` | Ketapang | Eurasia | Austronesian | — | — |
| `kjh` | Khakas | Eurasia | Altaic | — | — |
| `khg` | Kham (Tibetan) (Nangchen) | Eurasia | Sino-Tibetan | SOV | — |
| `kca` | Khanty | Eurasia | Uralic | SOV | — |
| `kjg` | Khmu' | Eurasia | Austro-Asiatic | SVO | — |
| `kfb` | Kolami | Eurasia | Dravidian | SOV | — |
| `kpy` | Koryak | Eurasia | Chukotko-Kamchatkan | SOV | — |
| `kle` | Kulung | Eurasia | Sino-Tibetan | — | — |
| `kum` | Kumyk | Eurasia | Altaic | — | — |
| `kru` | Kurukh | Eurasia | Dravidian | — | — |
| `kxv` | Kuvi | Eurasia | Dravidian | SOV | — |
| `lbj` | Ladakhi | Eurasia | Sino-Tibetan | SOV | — |
| `lhu` | Lahu | Eurasia | Sino-Tibetan | SOV | — |
| `lif` | Limbu | Eurasia | Sino-Tibetan | — | — |
| `lis` | Lisu | Eurasia | Sino-Tibetan | SOV | — |
| `nst` | Lungchang | Eurasia | Sino-Tibetan | — | — |
| `mhr` | Mari (Meadow) | Eurasia | Uralic | — | — |
| `mhx` | Maru | Eurasia | Sino-Tibetan | SOV | — |
| `nan` | Min (Southern) | Eurasia | Sino-Tibetan | — | — |
| `unr` | Mundari | Eurasia | Austro-Asiatic | SOV | — |
| `nag` | Naga Pidgin | Eurasia | other | — | — |
| `gld` | Nanai | Eurasia | Altaic | — | — |
| `nxq` | Naxi | Eurasia | Sino-Tibetan | — | — |
| `xal` | Oirat | Eurasia | Altaic | SOV | — |
| `oss` | Ossetic | Eurasia | Indo-European | SOV | — |
| `prk` | Parauk | Eurasia | Austro-Asiatic | — | — |
| `peg` | Pengo | Eurasia | Dravidian | — | — |
| `pww` | Phlong | Eurasia | Sino-Tibetan | — | — |
| `raw` | Rawang | Eurasia | Sino-Tibetan | SOV | — |
| `rmo` | Romani (Burgenland) | Eurasia | Indo-European | — | — |
| `sea` | Semai | Eurasia | Austro-Asiatic | — | — |
| `sza` | Semelai | Eurasia | Austro-Asiatic | No dominant order | — |
| `xsr` | Sherpa | Eurasia | Sino-Tibetan | SOV | — |
| `evn` | Solon | Eurasia | Altaic | — | — |
| `suv` | Sulung | Eurasia | Sino-Tibetan | — | — |
| `tly` | Talysh (Azerbaijan) | Eurasia | Indo-European | — | — |
| `taj` | Tamang (Eastern) | Eurasia | Sino-Tibetan | SOV | — |
| `tcz` | Thadou | Eurasia | Sino-Tibetan | — | — |
| `tkr` | Tsakhur | Eurasia | Nakh-Daghestanian | — | — |
| `urk` | Urak Lawoi' | Eurasia | Austronesian | SVO | — |
| `kpv` | Yazva | Eurasia | Uralic | — | — |
| `ess` | Yupik (Siberian) | Eurasia | Eskimo-Aleut | No dominant order | — |
| `nog` | Yurt Tatar | Eurasia | Altaic | — | — |
| `pjt` | Western Desert (Ooldea) | Oceanía | Pama-Nyungan | — | — |
| `agd` | Agarabi | Papúa y Oceanía | Trans-New Guinea | SOV | — |
| `alp` | Alune | Papúa y Oceanía | Austronesian | SVO | — |
| `amk` | Ambai | Papúa y Oceanía | Austronesian | SVO | — |
| `ami` | Amis | Papúa y Oceanía | Austronesian | No dominant order | — |
| `agg` | Anggor | Papúa y Oceanía | Senagi | SOV | — |
| `atq` | Aralle-Tabulahan | Papúa y Oceanía | Austronesian | — | — |
| `apr` | Arop-Lokep | Papúa y Oceanía | Austronesian | SVO | — |
| `aia` | Arosi | Papúa y Oceanía | Austronesian | SVO | — |
| `upv` | Atchin | Papúa y Oceanía | Austronesian | — | — |
| `awb` | Awa | Papúa y Oceanía | Trans-New Guinea | SOV | — |
| `blz` | Balantak | Papúa y Oceanía | Austronesian | — | — |
| `ptu` | Bambam | Papúa y Oceanía | Austronesian | — | — |
| `bdg` | Banggi | Papúa y Oceanía | Austronesian | SVO | — |
| `bbb` | Barai | Papúa y Oceanía | Trans-New Guinea | SOV | — |
| `byr` | Baruya | Papúa y Oceanía | Trans-New Guinea | — | — |
| `bvz` | Bauzi | Papúa y Oceanía | Geelvink Bay | SOV | — |
| `dbj` | Begak-Ida'an | Papúa y Oceanía | Austronesian | — | — |
| `bcl` | Bikol | Papúa y Oceanía | Austronesian | — | — |
| `bpr` | Bilaan (Koronadal) | Papúa y Oceanía | Austronesian | — | — |
| `bkd` | Binukid | Papúa y Oceanía | Austronesian | — | — |
| `bjr` | Binumarien | Papúa y Oceanía | Trans-New Guinea | — | — |
| `bis` | Bislama | Papúa y Oceanía | other | — | — |
| `bmu` | Burum | Papúa y Oceanía | Trans-New Guinea | — | — |
| `kzf` | Da'a | Papúa y Oceanía | Austronesian | — | — |
| `eip` | Eipo | Papúa y Oceanía | Trans-New Guinea | SOV | — |
| `frd` | Fordata | Papúa y Oceanía | Austronesian | — | — |
| `gbi` | Galela | Papúa y Oceanía | North Halmaheran | — | — |
| `pwg` | Gapapaiwa | Papúa y Oceanía | Austronesian | SOV | — |
| `nlg` | Gela | Papúa y Oceanía | Austronesian | VOS | — |
| `gor` | Gorontalo | Papúa y Oceanía | Austronesian | — | — |
| `hnn` | Hanunóo | Papúa y Oceanía | Austronesian | — | — |
| `had` | Hatam | Papúa y Oceanía | Hatim-Mansim | SVO | — |
| `ifb` | Ifugao (Batad) | Papúa y Oceanía | Austronesian | — | — |
| `itv` | Itawis | Papúa y Oceanía | Austronesian | — | — |
| `lew` | Kaili | Papúa y Oceanía | Austronesian | — | — |
| `kbq` | Kamano-Kafe | Papúa y Oceanía | Trans-New Guinea | — | — |
| `kne` | Kankanay | Papúa y Oceanía | Austronesian | — | — |
| `pss` | Kaulong | Papúa y Oceanía | Austronesian | SVO | — |
| `xte` | Ketengban | Papúa y Oceanía | Trans-New Guinea | — | — |
| `kij` | Kilivila | Papúa y Oceanía | Austronesian | No dominant order | — |
| `geb` | Kire | Papúa y Oceanía | Ramu-Lower Sepik | SOV | — |
| `gil` | Kiribati | Papúa y Oceanía | Austronesian | VOS | — |
| `kje` | Kisar | Papúa y Oceanía | Austronesian | — | — |
| `kvw` | Kolana | Papúa y Oceanía | Greater West Bomberai | — | — |
| `mbt` | Kulamanen | Papúa y Oceanía | Austronesian | — | — |
| `kue` | Kuman | Papúa y Oceanía | Trans-New Guinea | SOV | — |
| `kwd` | Kwaio | Papúa y Oceanía | Austronesian | SVO | — |
| `tnk` | Kwamera | Papúa y Oceanía | Austronesian | — | — |
| `kyc` | Kyaka | Papúa y Oceanía | Trans-New Guinea | SOV | — |
| `ljp` | Lampung | Papúa y Oceanía | Austronesian | SVO | — |
| `law` | Lauje | Papúa y Oceanía | Austronesian | — | — |
| `lnd` | Lun Dayeh | Papúa y Oceanía | Austronesian | — | — |
| `mhy` | Ma'anyan | Papúa y Oceanía | Austronesian | SVO | — |
| `xmm` | Manadonese | Papúa y Oceanía | Austronesian | SVO | — |
| `mbb` | Manobo (Western Bukidnon) | Papúa y Oceanía | Austronesian | VSO | — |
| `ayz` | Maybrat | Papúa y Oceanía | Maybrat | SVO | — |
| `mej` | Meyah | Papúa y Oceanía | East Bird's Head | SVO | — |
| `npy` | Napu | Papúa y Oceanía | Austronesian | — | — |
| `nas` | Nasioi | Papúa y Oceanía | South Bougainville | SOV | — |
| `nia` | Nias | Papúa y Oceanía | Austronesian | VOS | — |
| `ury` | Orya | Papúa y Oceanía | Tor-Kwerba | SOV | — |
| `pau` | Palauan | Papúa y Oceanía | Austronesian | SVO | — |
| `pmf` | Pamona | Papúa y Oceanía | Austronesian | — | — |
| `nij` | Pulopetak | Papúa y Oceanía | Austronesian | — | — |
| `rap` | Rapanui | Papúa y Oceanía | Austronesian | VSO | — |
| `rej` | Rejang | Papúa y Oceanía | Austronesian | — | — |
| `rro` | Roro | Papúa y Oceanía | Austronesian | — | — |
| `rug` | Roviana | Papúa y Oceanía | Austronesian | VSO | — |
| `apb` | Sa'a | Papúa y Oceanía | Austronesian | — | — |
| `saj` | Sahu | Papúa y Oceanía | North Halmaheran | SVO | — |
| `sxn` | Sangir | Papúa y Oceanía | Austronesian | — | — |
| `hvn` | Sawu | Papúa y Oceanía | Austronesian | — | — |
| `slu` | Selaru | Papúa y Oceanía | Austronesian | — | — |
| `snp` | Siane | Papúa y Oceanía | Trans-New Guinea | SOV | — |
| `tgo` | Sudest | Papúa y Oceanía | Austronesian | SVO | — |
| `tby` | Tabaru | Papúa y Oceanía | North Halmaheran | — | — |
| `tbg` | Tairora | Papúa y Oceanía | Trans-New Guinea | SOV | — |
| `tbc` | Takia | Papúa y Oceanía | Austronesian | SOV | — |
| `tbl` | Tboli | Papúa y Oceanía | Austronesian | VSO | — |
| `kps` | Tehit | Papúa y Oceanía | West Bird's Head | — | — |
| `aoz` | Timorese | Papúa y Oceanía | Austronesian | — | — |
| `tih` | Timugon | Papúa y Oceanía | Austronesian | VSO | — |
| `tlb` | Tobelo | Papúa y Oceanía | North Halmaheran | SOV | — |
| `tnt` | Tontemboan | Papúa y Oceanía | Austronesian | — | — |
| `sda` | Toraja | Papúa y Oceanía | Austronesian | — | — |
| `ppk` | Uma | Papúa y Oceanía | Austronesian | — | — |
| `urt` | Urat | Papúa y Oceanía | Torricelli | SVO | — |
| `lex` | Wetan | Papúa y Oceanía | Austronesian | — | — |
| `wlo` | Wolio | Papúa y Oceanía | Austronesian | VSO | — |
| `yka` | Yakan | Papúa y Oceanía | Austronesian | — | — |
| `yli` | Yali | Papúa y Oceanía | Trans-New Guinea | — | — |
| `jmd` | Yamdena | Papúa y Oceanía | Austronesian | — | — |
| `tao` | Yami | Papúa y Oceanía | Austronesian | — | — |
| `yva` | Yawa | Papúa y Oceanía | Yawa | — | — |
| `abi` | Abidji | África | Niger-Congo | — | — |
| `adj` | Adioukrou | África | Niger-Congo | SVO | — |
| `any` | Anyi | África | Niger-Congo | SVO | — |
| `avn` | Avatime | África | Niger-Congo | — | — |
| `avu` | Avokaya | África | Central Sudanic | No dominant order | — |
| `bav` | Babungo | África | Niger-Congo | SVO | — |
| `bdh` | Baka (in South Sudan) | África | Central Sudanic | SVO | — |
| `bcw` | Bana | África | Afro-Asiatic | — | — |
| `bba` | Bariba | África | Niger-Congo | — | — |
| `bsc` | Basari | África | Niger-Congo | — | — |
| `bng` | Benga | África | Niger-Congo | — | — |
| `bim` | Bimoba | África | Niger-Congo | SVO | — |
| `bom` | Birom | África | Niger-Congo | SVO | — |
| `bib` | Bisa | África | Mande | — | — |
| `bbo` | Bobo Madaré (Northern) | África | Mande | — | — |
| `bqc` | Boko | África | Mande | SOV | — |
| `bwu` | Buli (in Ghana) | África | Niger-Congo | SVO | — |
| `bqp` | Busa | África | Mande | SOV | — |
| `old` | Chaga | África | Niger-Congo | SVO | — |
| `ncu` | Chumburung | África | Niger-Congo | — | — |
| `dbq` | Daba | África | Afro-Asiatic | — | — |
| `dga` | Dagaare | África | Niger-Congo | SVO | — |
| `daa` | Dangaléat (Western) | África | Afro-Asiatic | — | — |
| `tcc` | Datooga | África | Eastern Sudanic | — | — |
| `dsh` | Dhaasanac | África | Afro-Asiatic | SOV | — |
| `did` | Didinga | África | Eastern Sudanic | VSO | — |
| `dyo` | Diola-Fogny | África | Niger-Congo | SVO | — |
| `dyi` | Dyimini | África | Niger-Congo | — | — |
| `gmv` | Gamo | África | Afro-Asiatic | SOV | — |
| `gso` | Gbaya (Southwest) | África | Niger-Congo | SVO | — |
| `gkn` | Gokana | África | Niger-Congo | SVO | — |
| `gde` | Gude | África | Afro-Asiatic | VSO | — |
| `guk` | Gumuz | África | Gumuz | SVO | — |
| `yas` | Gunu | África | Niger-Congo | — | — |
| `gux` | Gurma | África | Niger-Congo | — | — |
| `kcg` | Gworok | África | Niger-Congo | SVO | — |
| `amf` | Hamer | África | Afro-Asiatic | — | — |
| `hay` | Haya | África | Niger-Congo | SVO | — |
| `xed` | Hdi | África | Afro-Asiatic | VSO | — |
| `heh` | Hehe | África | Niger-Congo | SVO | — |
| `ilb` | Ila | África | Niger-Congo | SVO | — |
| `irk` | Iraqw | África | Afro-Asiatic | SOV | — |
| `izr` | Izere | África | Niger-Congo | SVO | — |
| `izz` | Izi | África | Niger-Congo | SVO | — |
| `jbu` | Jukun | África | Niger-Congo | SVO | — |
| `bex` | Jur Mödö | África | Central Sudanic | SVO | — |
| `kbp` | Kabiyé | África | Niger-Congo | SVO | — |
| `kab` | Kabyle | África | Afro-Asiatic | VSO | — |
| `kki` | Kagulu | África | Niger-Congo | — | — |
| `kdj` | Karimojong | África | Eastern Sudanic | VSO | — |
| `xsm` | Kasem | África | Niger-Congo | SVO | — |
| `kbr` | Kefa | África | Afro-Asiatic | — | — |
| `kyq` | Kenga | África | Central Sudanic | SVO | — |
| `ken` | Kenyang | África | Niger-Congo | — | — |
| `ker` | Kera | África | Afro-Asiatic | SVO | — |
| `kik` | Kikuyu | África | Niger-Congo | SVO | — |
| `zga` | Kinga | África | Niger-Congo | SVO | — |
| `kss` | Kisi (Southern) | África | Niger-Congo | — | — |
| `klu` | Klao | África | Niger-Congo | SVO | — |
| `xuo` | Koh | África | Niger-Congo | — | — |
| `xon` | Konkomba | África | Niger-Congo | — | — |
| `kma` | Konni | África | Niger-Congo | SVO | — |
| `kqy` | Koorete | África | Afro-Asiatic | — | — |
| `knk` | Koranko | África | Mande | — | — |
| `kia` | Kosop | África | Niger-Congo | — | — |
| `khq` | Koyra Chiini | África | Songhay | SVO | — |
| `ses` | Koyraboro Senni | África | Songhay | SOV | — |
| `krs` | Kresh | África | Central Sudanic | SVO | — |
| `bfa` | Kukú | África | Eastern Sudanic | — | — |
| `dwr` | Kullo | África | Afro-Asiatic | — | — |
| `lam` | Lamba | África | Niger-Congo | No dominant order | — |
| `lns` | Lamnso' | África | Niger-Congo | — | — |
| `lme` | Lamé | África | Afro-Asiatic | — | — |
| `laj` | Lango | África | Eastern Sudanic | SVO | — |
| `lln` | Lele | África | Afro-Asiatic | SVO | — |
| `lef` | Lelemi | África | Niger-Congo | SVO | — |
| `lob` | Lobi | África | Niger-Congo | — | — |
| `lok` | Loko | África | Mande | — | — |
| `lom` | Loma | África | Mande | — | — |
| `bdu` | Londo | África | Niger-Congo | SVO | — |
| `lgg` | Lugbara | África | Central Sudanic | No dominant order | — |
| `lee` | Lyele | África | Niger-Congo | — | — |
| `mhi` | Ma'di | África | Central Sudanic | No dominant order | — |
| `mdy` | Maale | África | Afro-Asiatic | — | — |
| `mda` | Mada (in Nigeria) | África | Niger-Congo | — | — |
| `mcp` | Makaa | África | Niger-Congo | SVO | — |
| `kde` | Makonde | África | Niger-Congo | SVO | — |
| `mgh` | Makua | África | Niger-Congo | SVO | — |
| `maw` | Mampruli | África | Niger-Congo | — | — |
| `mge` | Mango | África | Central Sudanic | — | — |
| `knf` | Mankanya | África | Niger-Congo | — | — |
| `mev` | Mano | África | Mande | SOV | — |
| `men` | Mende | África | Mande | SOV | — |
| `mif` | Mofu-Gudur | África | Afro-Asiatic | SVO | — |
| `mgd` | Moru | África | Central Sudanic | No dominant order | — |
| `sgw` | Muher | África | Afro-Asiatic | — | — |
| `mzm` | Mumuye | África | Niger-Congo | SVO | — |
| `sur` | Mupun | África | Afro-Asiatic | SVO | — |
| `nfr` | Nafaanra | África | Niger-Congo | — | — |
| `nnb` | Nande | África | Niger-Congo | — | — |
| `ntm` | Nateni | África | Niger-Congo | — | — |
| `bud` | Ncàm | África | Niger-Congo | SVO | — |
| `ndz` | Ndogo | África | Niger-Congo | — | — |
| `ndv` | Ndut | África | Niger-Congo | SVO | — |
| `sba` | Ngambay | África | Central Sudanic | SVO | — |
| `nga` | Ngbaka (Minagende) | África | Niger-Congo | SVO | — |
| `pcm` | Nigerian Pidgin | África | other | — | — |
| `nko` | Nkonya | África | Niger-Congo | SVO | — |
| `nhu` | Noni | África | Niger-Congo | SVO | — |
| `ann` | Obolo | África | Niger-Congo | SVO | — |
| `oku` | Oku | África | Niger-Congo | — | — |
| `asa` | Pare | África | Niger-Congo | SVO | — |
| `pbi` | Podoko | África | Afro-Asiatic | VSO | — |
| `poy` | Pogoro | África | Niger-Congo | SVO | — |
| `rel` | Rendille | África | Afro-Asiatic | — | — |
| `rim` | Rimi | África | Niger-Congo | SVO | — |
| `rng` | Ronga | África | Niger-Congo | SVO | — |
| `run` | Rundi | África | Niger-Congo | — | — |
| `nyn` | Runyankore | África | Niger-Congo | SVO | — |
| `nyo` | Runyoro-Rutooro | África | Niger-Congo | SVO | — |
| `sag` | Sango | África | Niger-Congo | SVO | — |
| `kpz` | Sebei | África | Eastern Sudanic | VSO | — |
| `seh` | Sena | África | Niger-Congo | — | — |
| `ksb` | Shambala | África | Niger-Congo | SVO | — |
| `shk` | Shilluk | África | Eastern Sudanic | SVO | — |
| `sid` | Sidaama | África | Afro-Asiatic | SOV | — |
| `sil` | Sisaala | África | Niger-Congo | SVO | — |
| `suk` | Sukuma | África | Niger-Congo | SVO | — |
| `spp` | Supyire | África | Niger-Congo | SOV | — |
| `tap` | Tabwa | África | Niger-Congo | SVO | — |
| `tlj` | Talinga | África | Niger-Congo | SVO | — |
| `taq` | Tamashek | África | Afro-Asiatic | VSO | — |
| `tpm` | Tampulma | África | Niger-Congo | — | — |
| `shi` | Tashlhiyt | África | Afro-Asiatic | No dominant order | — |
| `kdh` | Tem | África | Niger-Congo | — | — |
| `tem` | Temne | África | Niger-Congo | SVO | — |
| `tex` | Tennet | África | Eastern Sudanic | VSO | — |
| `teo` | Teso | África | Eastern Sudanic | VSO | — |
| `tik` | Tikar | África | Niger-Congo | No dominant order | — |
| `dts` | Toro So | África | Dogon | — | — |
| `tso` | Tsonga | África | Niger-Congo | — | — |
| `tmc` | Tumak | África | Afro-Asiatic | — | — |
| `vag` | Vagla | África | Niger-Congo | — | — |
| `vif` | Vili | África | Niger-Congo | — | — |
| `wwa` | Waama | África | Niger-Congo | SVO | — |
| `wob` | Wobe | África | Niger-Congo | — | — |
| `kao` | Xasonga | África | Mande | SOV | — |
| `yam` | Yamba | África | Niger-Congo | — | — |
| `yao` | Yao (in Malawi) | África | Niger-Congo | SVO | — |
| `ybb` | Yemba | África | Niger-Congo | — | — |
| `zne` | Zande | África | Niger-Congo | SVO | — |
| `maz-ixc` | Mazateco de Ixcatlán | — | — | — | — |
| `mzi` | Mazateco de Ixcatlán | — | — | — | — |
| `maj` | Mazateco de Jalapa de Díaz | — | — | — | — |
| `maz-jal` | Mazateco de Jalapa de Díaz | — | — | — | — |
| `mix` | Mixteco de Alcozauca | — | — | — | — |
| `xta` | Mixteco de Alcozauca | — | — | — | — |
| `mix-ata` | Mixteco de Atatlahuca | — | — | — | — |
| `nah-mor` | Náhuatl Huasteca Central | — | — | — | — |
| `nch` | Náhuatl Huasteca Central | — | — | — | — |
| `nah-gro` | Náhuatl de Guerrero | — | — | — | — |
| `nah-mic` | Náhuatl de Michoacán | — | — | — | — |
| `nah-tla` | Náhuatl de Tlamacazapa | — | — | — | — |
| `nuz` | Náhuatl de Tlamacazapa | — | — | — | — |
| `nah` | Náhuatl de Zacapoaxtla | — | — | — | — |
| `nah-oax` | Náhuatl del Norte de Oaxaca | — | — | — | — |
| `nhy` | Náhuatl del Norte de Oaxaca | — | — | — | — |
| `oto` | Otomí de Querétaro | — | — | — | — |
| `pls` | Popoloca | — | — | — | — |
| `tpp` | Tepehua | — | — | — | — |
| `toc` | Totonaco | — | — | — | — |
| `tri-chi` | Triqui de Chicahuaxtla | — | — | — | — |
| `zap-sie` | Zapoteco de la Sierra | — | — | — | — |
| `zap-val` | Zapoteco del Valle | — | — | — | — |
| `abp` | — | — | — | — | — |
| `acd` | — | — | — | — | — |
| `acf` | — | — | — | — | — |
| `ade` | — | — | — | — | — |
| `adh` | — | — | — | — | — |
| `aeu` | — | — | — | — | — |
| `agn` | — | — | — | — | — |
| `aha` | — | — | — | — | — |
| `akb` | — | — | — | — | — |
| `akp` | — | — | — | — | — |
| `alj` | — | — | — | — | — |
| `asg` | — | — | — | — | — |
| `ata` | — | — | — | — | — |
| `atb` | — | — | — | — | — |
| `atg` | — | — | — | — | — |
| `ati` | — | — | — | — | — |
| `azg` | — | — | — | — | — |
| `azj-script_cyrillic` | — | — | — | — | — |
| `bcc-script_arabic` | — | — | — | — | — |
| `bcc-script_latin` | — | — | — | — | — |
| `bdv` | — | — | — | — | — |
| `beh` | — | — | — | — | — |
| `bep` | — | — | — | — | — |
| `bfo` | — | — | — | — | — |
| `bfy` | — | — | — | — | — |
| `bfz` | — | — | — | — | — |
| `bgc` | — | — | — | — | — |
| `bgt` | — | — | — | — | — |
| `bgw` | — | — | — | — | — |
| `bha` | — | — | — | — | — |
| `bht` | — | — | — | — | — |
| `bhz` | — | — | — | — | — |
| `biv` | — | — | — | — | — |
| `bjv` | — | — | — | — | — |
| `bjw` | — | — | — | — | — |
| `bjz` | — | — | — | — | — |
| `bkv` | — | — | — | — | — |
| `blh` | — | — | — | — | — |
| `blt` | — | — | — | — | — |
| `blx` | — | — | — | — | — |
| `bmq` | — | — | — | — | — |
| `bmv` | — | — | — | — | — |
| `bno` | — | — | — | — | — |
| `bnp` | — | — | — | — | — |
| `boj` | — | — | — | — | — |
| `bov` | — | — | — | — | — |
| `box` | — | — | — | — | — |
| `bps` | — | — | — | — | — |
| `bqi` | — | — | — | — | — |
| `bqj` | — | — | — | — | — |
| `bsq` | — | — | — | — | — |
| `bss` | — | — | — | — | — |
| `btd` | — | — | — | — | — |
| `btt` | — | — | — | — | — |
| `bus` | — | — | — | — | — |
| `bvc` | — | — | — | — | — |
| `bwq` | — | — | — | — | — |
| `bzh` | — | — | — | — | — |
| `bzi` | — | — | — | — | — |
| `bzj` | — | — | — | — | — |
| `cac-dialect_sanmateoixtatan` | — | — | — | — | — |
| `cac-dialect_sansebastiancoatan` | — | — | — | — | — |
| `cak-dialect_central` | — | — | — | — | — |
| `cak-dialect_santamariadejesus` | — | — | — | — | — |
| `cak-dialect_santodomingoxenacoj` | — | — | — | — | — |
| `cak-dialect_southcentral` | — | — | — | — | — |
| `cak-dialect_western` | — | — | — | — | — |
| `cak-dialect_yepocapa` | — | — | — | — | — |
| `cwe` | — | — | — | — | — |
| `cwt` | — | — | — | — | — |
| `dah` | — | — | — | — | — |
| `ddn` | — | — | — | — | — |
| `ded` | — | — | — | — | — |
| `dgi` | — | — | — | — | — |
| `dgk` | — | — | — | — | — |
| `dgr` | — | — | — | — | — |
| `dig` | — | — | — | — | — |
| `dik` | — | — | — | — | — |
| `dip` | — | — | — | — | — |
| `dnj-dialect_blowowest` | — | — | — | — | — |
| `dnj-dialect_gweetaawueast` | — | — | — | — | — |
| `dnt` | — | — | — | — | — |
| `dnw` | — | — | — | — | — |
| `dop` | — | — | — | — | — |
| `dos` | — | — | — | — | — |
| `dso` | — | — | — | — | — |
| `dtp` | — | — | — | — | — |
| `dug` | — | — | — | — | — |
| `dzo` | — | — | — | — | — |
| `eka` | — | — | — | — | — |
| `enb` | — | — | — | — | — |
| `eza` | — | — | — | — | — |
| `fal` | — | — | — | — | — |
| `far` | — | — | — | — | — |
| `flr` | — | — | — | — | — |
| `fmu` | — | — | — | — | — |
| `ful` | — | — | — | — | — |
| `gag-script_cyrillic` | — | — | — | — | — |
| `gag-script_latin` | — | — | — | — | — |
| `gai` | — | — | — | — | — |
| `gam` | — | — | — | — | — |
| `gau` | — | — | — | — | — |
| `gbk` | — | — | — | — | — |
| `gbm` | — | — | — | — | — |
| `gbo` | — | — | — | — | — |
| `gej` | — | — | — | — | — |
| `gjn` | — | — | — | — | — |
| `gna` | — | — | — | — | — |
| `gnd` | — | — | — | — | — |
| `gng` | — | — | — | — | — |
| `gof-script_latin` | — | — | — | — | — |
| `gog` | — | — | — | — | — |
| `gqr` | — | — | — | — | — |
| `grc` | — | — | — | — | — |
| `gri` | — | — | — | — | — |
| `gud` | — | — | — | — | — |
| `guu` | — | — | — | — | — |
| `gvl` | — | — | — | — | — |
| `gwr` | — | — | — | — | — |
| `gyr` | — | — | — | — | — |
| `hag` | — | — | — | — | — |
| `hap` | — | — | — | — | — |
| `hif` | — | — | — | — | — |
| `hig` | — | — | — | — | — |
| `hlt` | — | — | — | — | — |
| `hne` | — | — | — | — | — |
| `hns` | — | — | — | — | — |
| `hoy` | — | — | — | — | — |
| `hui` | — | — | — | — | — |
| `hus-dialect_centralveracruz` | — | — | — | — | — |
| `hus-dialect_westernpotosino` | — | — | — | — | — |
| `icr` | — | — | — | — | — |
| `idd` | — | — | — | — | — |
| `ifa` | — | — | — | — | — |
| `ife` | — | — | — | — | — |
| `ifk` | — | — | — | — | — |
| `ifu` | — | — | — | — | — |
| `ify` | — | — | — | — | — |
| `ikk` | — | — | — | — | — |
| `imo` | — | — | — | — | — |
| `iou` | — | — | — | — | — |
| `ipi` | — | — | — | — | — |
| `iqw` | — | — | — | — | — |
| `iri` | — | — | — | — | — |
| `ixl-dialect_sangasparchajul` | — | — | — | — | — |
| `ixl-dialect_sanjuancotzal` | — | — | — | — | — |
| `ixl-dialect_santamarianebaj` | — | — | — | — | — |
| `jen` | — | — | — | — | — |
| `jmc` | — | — | — | — | — |
| `juy` | — | — | — | — | — |
| `jvn` | — | — | — | — | — |
| `kak` | — | — | — | — | — |
| `kbo` | — | — | — | — | — |
| `kby` | — | — | — | — | — |
| `kdc` | — | — | — | — | — |
| `kdi` | — | — | — | — | — |
| `kdl` | — | — | — | — | — |
| `kdn` | — | — | — | — | — |
| `kdt` | — | — | — | — | — |
| `keo` | — | — | — | — | — |
| `key` | — | — | — | — | — |
| `kez` | — | — | — | — | — |
| `kff-script_telugu` | — | — | — | — | — |
| `kfw` | — | — | — | — | — |
| `kfx` | — | — | — | — | — |
| `kkj` | — | — | — | — | — |
| `klv` | — | — | — | — | — |
| `klw` | — | — | — | — | — |
| `kmd` | — | — | — | — | — |
| `kml` | — | — | — | — | — |
| `kmr-script_arabic` | — | — | — | — | — |
| `kmr-script_cyrillic` | — | — | — | — | — |
| `kmr-script_latin` | — | — | — | — | — |
| `kmu` | — | — | — | — | — |
| `knb` | — | — | — | — | — |
| `kno` | — | — | — | — | — |
| `kpq` | — | — | — | — | — |
| `kqe` | — | — | — | — | — |
| `kqp` | — | — | — | — | — |
| `kqr` | — | — | — | — | — |
| `krj` | — | — | — | — | — |
| `krr` | — | — | — | — | — |
| `ksr` | — | — | — | — | — |
| `ktb` | — | — | — | — | — |
| `ktj` | — | — | — | — | — |
| `kub` | — | — | — | — | — |
| `kus` | — | — | — | — | — |
| `kwf` | — | — | — | — | — |
| `kxc` | — | — | — | — | — |
| `kxf` | — | — | — | — | — |
| `kxm` | — | — | — | — | — |
| `kyb` | — | — | — | — | — |
| `kyf` | — | — | — | — | — |
| `kyg` | — | — | — | — | — |
| `kyo` | — | — | — | — | — |
| `kyu` | — | — | — | — | — |
| `las` | — | — | — | — | — |
| `lat` | — | — | — | — | — |
| `lbw` | — | — | — | — | — |
| `lcp` | — | — | — | — | — |
| `lem` | — | — | — | — | — |
| `lgl` | — | — | — | — | — |
| `lia` | — | — | — | — | — |
| `lid` | — | — | — | — | — |
| `lip` | — | — | — | — | — |
| `lje` | — | — | — | — | — |
| `llg` | — | — | — | — | — |
| `lon` | — | — | — | — | — |
| `loq` | — | — | — | — | — |
| `lsi` | — | — | — | — | — |
| `lsm` | — | — | — | — | — |
| `luc` | — | — | — | — | — |
| `mbh` | — | — | — | — | — |
| `mbu` | — | — | — | — | — |
| `mbz` | — | — | — | — | — |
| `mcq` | — | — | — | — | — |
| `mcu` | — | — | — | — | — |
| `mdv` | — | — | — | — | — |
| `med` | — | — | — | — | — |
| `mee` | — | — | — | — | — |
| `meq` | — | — | — | — | — |
| `met` | — | — | — | — | — |
| `mfh` | — | — | — | — | — |
| `mfi` | — | — | — | — | — |
| `mfk` | — | — | — | — | — |
| `mfq` | — | — | — | — | — |
| `mfz` | — | — | — | — | — |
| `mgo` | — | — | — | — | — |
| `myx` | — | — | — | — | — |
| `mza` | — | — | — | — | — |
| `mzj` | — | — | — | — | — |
| `mzk` | — | — | — | — | — |
| `mzw` | — | — | — | — | — |
| `naw` | — | — | — | — | — |
| `nca` | — | — | — | — | — |
| `ndj` | — | — | — | — | — |
| `ndp` | — | — | — | — | — |
| `ndy` | — | — | — | — | — |
| `neb` | — | — | — | — | — |
| `nfa` | — | — | — | — | — |
| `ngl` | — | — | — | — | — |
| `ngp` | — | — | — | — | — |
| `nhi` | — | — | — | — | — |
| `nhw` | — | — | — | — | — |
| `nim` | — | — | — | — | — |
| `nin` | — | — | — | — | — |
| `nlc` | — | — | — | — | — |
| `nlk` | — | — | — | — | — |
| `nmz` | — | — | — | — | — |
| `nnq` | — | — | — | — | — |
| `nnw` | — | — | — | — | — |
| `nod` | — | — | — | — | — |
| `npl` | — | — | — | — | — |
| `nsu` | — | — | — | — | — |
| `ntr` | — | — | — | — | — |
| `nuj` | — | — | — | — | — |
| `nwb` | — | — | — | — | — |
| `nyf` | — | — | — | — | — |
| `nyy` | — | — | — | — | — |
| `nzi` | — | — | — | — | — |
| `obo` | — | — | — | — | — |
| `ojb-script_latin` | — | — | — | — | — |
| `ojb-script_syllabics` | — | — | — | — | — |
| `omw` | — | — | — | — | — |
| `onb` | — | — | — | — | — |
| `ozm` | — | — | — | — | — |
| `pbc` | — | — | — | — | — |
| `pce` | — | — | — | — | — |
| `pez` | — | — | — | — | — |
| `pil` | — | — | — | — | — |
| `pis` | — | — | — | — | — |
| `pkb` | — | — | — | — | — |
| `plw` | — | — | — | — | — |
| `pny` | — | — | — | — | — |
| `poh-dialect_eastern` | — | — | — | — | — |
| `poh-dialect_western` | — | — | — | — | — |
| `pps` | — | — | — | — | — |
| `prf` | — | — | — | — | — |
| `prt` | — | — | — | — | — |
| `pse` | — | — | — | — | — |
| `pxm` | — | — | — | — | — |
| `quc-dialect_central` | — | — | — | — | — |
| `quc-dialect_east` | — | — | — | — | — |
| `quc-dialect_north` | — | — | — | — | — |
| `quf` | — | — | — | — | — |
| `qul` | — | — | — | — | — |
| `quw` | — | — | — | — | — |
| `qve` | — | — | — | — | — |
| `qvh` | — | — | — | — | — |
| `qvm` | — | — | — | — | — |
| `qvo` | — | — | — | — | — |
| `qvs` | — | — | — | — | — |
| `qvw` | — | — | — | — | — |
| `qvz` | — | — | — | — | — |
| `qwh` | — | — | — | — | — |
| `qxh` | — | — | — | — | — |
| `qxl` | — | — | — | — | — |
| `qxn` | — | — | — | — | — |
| `qxo` | — | — | — | — | — |
| `qxr` | — | — | — | — | — |
| `rah` | — | — | — | — | — |
| `rai` | — | — | — | — | — |
| `rav` | — | — | — | — | — |
| `rgu` | — | — | — | — | — |
| `rhg` | — | — | — | — | — |
| `rif-script_arabic` | — | — | — | — | — |
| `rif-script_latin` | — | — | — | — | — |
| `ril` | — | — | — | — | — |
| `rjs` | — | — | — | — | — |
| `rkt` | — | — | — | — | — |
| `rmc-script_cyrillic` | — | — | — | — | — |
| `rmc-script_latin` | — | — | — | — | — |
| `rmy-script_cyrillic` | — | — | — | — | — |
| `rmy-script_latin` | — | — | — | — | — |
| `rnl` | — | — | — | — | — |
| `rol` | — | — | — | — | — |
| `rub` | — | — | — | — | — |
| `ruf` | — | — | — | — | — |
| `saq` | — | — | — | — | — |
| `sas` | — | — | — | — | — |
| `sbd` | — | — | — | — | — |
| `sbl` | — | — | — | — | — |
| `sbp` | — | — | — | — | — |
| `sch` | — | — | — | — | — |
| `sck` | — | — | — | — | — |
| `sgb` | — | — | — | — | — |
| `sgj` | — | — | — | — | — |
| `sho` | — | — | — | — | — |
| `sig` | — | — | — | — | — |
| `sjm` | — | — | — | — | — |
| `sld` | — | — | — | — | — |
| `sml` | — | — | — | — | — |
| `sne` | — | — | — | — | — |
| `snw` | — | — | — | — | — |
| `soy` | — | — | — | — | — |
| `spy` | — | — | — | — | — |
| `srx` | — | — | — | — | — |
| `stn` | — | — | — | — | — |
| `suc` | — | — | — | — | — |
| `suz` | — | — | — | — | — |
| `sxb` | — | — | — | — | — |
| `sya` | — | — | — | — | — |
| `syl` | — | — | — | — | — |
| `tbk` | — | — | — | — | — |
| `tbz` | — | — | — | — | — |
| `tdj` | — | — | — | — | — |
| `ted` | — | — | — | — | — |
| `tes` | — | — | — | — | — |
| `tgj` | — | — | — | — | — |
| `tgp` | — | — | — | — | — |
| `thk` | — | — | — | — | — |
| `thl` | — | — | — | — | — |
| `tmf` | — | — | — | — | — |
| `tng` | — | — | — | — | — |
| `tnn` | — | — | — | — | — |
| `tnp` | — | — | — | — | — |
| `tnr` | — | — | — | — | — |
| `toh` | — | — | — | — | — |
| `tom` | — | — | — | — | — |
| `trn` | — | — | — | — | — |
| `tte` | — | — | — | — | — |
| `ttq-script_tifinagh` | — | — | — | — | — |
| `tuk-script_arabic` | — | — | — | — | — |
| `udu` | — | — | — | — | — |
| `uig-script_cyrillic` | — | — | — | — | — |
| `urd-script_devanagari` | — | — | — | — | — |
| `urd-script_latin` | — | — | — | — | — |
| `usp` | — | — | — | — | — |
| `uzb-script_cyrillic` | — | — | — | — | — |
| `vid` | — | — | — | — | — |
| `vmw` | — | — | — | — | — |
| `vmy` | — | — | — | — | — |
| `vun` | — | — | — | — | — |
| `vut` | — | — | — | — | — |
| `wal-script_ethiopic` | — | — | — | — | — |
| `wal-script_latin` | — | — | — | — | — |
| `wlx` | — | — | — | — | — |
| `wmw` | — | — | — | — | — |
| `wsg` | — | — | — | — | — |
| `xnj` | — | — | — | — | — |
| `xnr` | — | — | — | — | — |
| `xog` | — | — | — | — | — |
| `xrb` | — | — | — | — | — |
| `xsb` | — | — | — | — | — |
| `xtd` | — | — | — | — | — |
| `xtm` | — | — | — | — | — |
| `xtn` | — | — | — | — | — |
| `xua` | — | — | — | — | — |
| `yal` | — | — | — | — | — |
| `yat` | — | — | — | — | — |
| `yaz` | — | — | — | — | — |
| `yba` | — | — | — | — | — |
| `ycl` | — | — | — | — | — |
| `yea` | — | — | — | — | — |
| `yre` | — | — | — | — | — |
| `zac` | — | — | — | — | — |
| `zad` | — | — | — | — | — |
| `zae` | — | — | — | — | — |
| `zam` | — | — | — | — | — |
| `zao` | — | — | — | — | — |
| `zaq` | — | — | — | — | — |
| `zar` | — | — | — | — | — |
| `zas` | — | — | — | — | — |
| `zca` | — | — | — | — | — |
| `zim` | — | — | — | — | — |
| `ziw` | — | — | — | — | — |
| `zmz` | — | — | — | — | — |
| `zpc` | — | — | — | — | — |
| `zpg` | — | — | — | — | — |
| `zpl` | — | — | — | — | — |
| `zpo` | — | — | — | — | — |
| `zpt` | — | — | — | — | — |
| `zpu` | — | — | — | — | — |
| `ztq` | — | — | — | — | — |
| `zty` | — | — | — | — | — |
| `zyb` | — | — | — | — | — |
| `zyp` | — | — | — | — | — |
| `zza` | — | — | — | — | — |


## 🔵 Tier C — solo texto — 3 lenguas

Sin checkpoint MMS: el sistema entrega traducción (si el LLM puede) pero NO genera audio. Candidatas a fine-tune propio con corpus consentido.

| ISO | Lengua | Región | Familia | Orden | Google |
|---|---|---|---|---|---|
| `hch` | Huichol | Américas | Uto-Aztecan | SOV | — |
| `tzh` | Tzeltal (Tenejapa) | Américas | Mayan | — | — |
| `tzo` | Tzotzil | Américas | Mayan | VOS | — |


## 🔴 Tier D — sin cobertura en el registro

Existen ~7,900 lenguas vivas en ISO 639-3; este registro cubre 1020 (las 999 con checkpoint MMS + 3 adicionales de WALS). El resto (~6,800) no tiene ni voz MMS ni datos tipológicos cargados — son el universo de trabajo para la fase de datasets comunitarios. Ver `docs/CUALQUIER_IDIOMA.md` para agregar cualquier ISO vía `languages_extra.json`.


## México — detalle por lengua

| ISO | Lengua | Tier | Google | Orden |
|---|---|---|---|---|
| `acr` | Achí | B | — | — |
| `agu` | Aguacatec | B | — | — |
| `cya` | Chatino (Nopala) | B | — | — |
| `caa` | Chortí | B | — | — |
| `hus` | Huastec | B | — | SVO |
| `hch` | Huichol | C | — | SOV |
| `jac` | Jakaltek | B | — | VSO |
| `kek` | K'ekchí | A | kek | — |
| `kjb` | Kanjobal (Eastern) | B | — | — |
| `knj` | Kanjobal (Western) | B | — | — |
| `lac` | Lacandón | B | — | No dominant order |
| `mam` | Mam | A | mam | VSO |
| `mfy` | Mayo | B | — | — |
| `maz` | Mazahua | B | — | — |
| `maq` | Mazatec (Chiquihuitlán) | B | — | — |
| `mim` | Mixtec (Alacatlatzala) | B | — | — |
| `mib` | Mixtec (Atatlahuca) | B | — | — |
| `mih` | Mixtec (Chayuco) | B | — | — |
| `mie` | Mixtec (Ocotepec) | B | — | VSO |
| `mil` | Mixtec (Peñoles) | B | — | VSO |
| `ncj` | Nahuatl (Huauchinango) | B | — | — |
| `nhx` | Nahuatl (Mecayapan Isthmus) | B | — | — |
| `ncl` | Nahuatl (Michoacán) | B | — | SVO |
| `azz` | Nahuatl (Sierra de Zacapoaxtla) | B | — | — |
| `ngu` | Nahuatl (Xalitla) | B | — | — |
| `ood` | O'odham | B | — | No dominant order |
| `ote` | Otomí (Mezquital) | B | — | VOS |
| `otq` | Otomí (Santiago Mexquititlan) | B | — | — |
| `pao` | Paiute (Northern) | B | — | SOV |
| `tac` | Tarahumara (Western) | B | — | SOV |
| `ttc` | Tectiteco | B | — | — |
| `tee` | Tepehua (Huehuetla) | B | — | No dominant order |
| `tpt` | Tepehua (Tlachichilco) | B | — | SVO |
| `stp` | Tepehuan (Southeastern) | B | — | — |
| `tos` | Totonac (Sierra) | B | — | — |
| `trs` | Trique (Chicahuaxtla) | B | — | — |
| `trc` | Trique (Copala) | B | — | VSO |
| `tzh` | Tzeltal (Tenejapa) | C | — | — |
| `tzo` | Tzotzil | C | — | VOS |
| `yua` | Yucatec | A | yua | — |
| `zai` | Zapotec (Isthmus) | A | zap | VSO |
| `zaa` | Zapotec (Juárez) | B | — | — |
| `zaw` | Zapotec (Mitla) | B | — | VSO |
| `zpm` | Zapotec (Mixtepec) | B | — | — |
| `zpi` | Zapotec (Quiegolani) | B | — | — |
| `zab` | Zapotec (San Lucas Quiaviní) | B | — | — |
| `zpz` | Zapotec (Texmelucan) | B | — | — |
| `zav` | Zapotec (Yatzachi) | B | — | — |
