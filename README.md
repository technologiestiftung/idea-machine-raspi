![](https://img.shields.io/badge/Built%20with%20%E2%9D%A4%EF%B8%8F-at%20Technologiestiftung%20Berlin-blue)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->

[![All Contributors](https://img.shields.io/badge/all_contributors-0-orange.svg?style=flat-square)](#contributors-)

<!-- ALL-CONTRIBUTORS-BADGE:END -->

# {repo-template}

## TODO (after you generated the repo)

- [ ] Review the content of the README.md and adjust to your liking
- [ ] Read the README.md till the end and adjust the content licensing,
      logos, etc (I know you stopped at tbd...)
- [ ] Adjust the file [.github/CODEOWNERS](./.github/CODEOWNERS)
- [ ] Adjust the files under [.github/ISSUE_TEMPLATE](./.github/ISSUE_TEMPLATE)
- [ ] If you use staging and main branches use this template for [.github/renovate.json](./.github/renovate.json)

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["github>technologiestiftung/renovate-config"],
  "baseBranches": ["staging"]
}
```

- [ ] Do you want to honor all kinds of contributions? Use [all-contributors](https://allcontributors.org/)

```bash
npx all-contributors-cli check
npx all-contributors-cli add github-name doc
```

You can use it on GitHub just by commenting on PRs and issues:

```plain
@all-contributors please add @github-name for infrastructure, tests and code
```

- [ ] Add your project description
- [ ] Get fancy shields at https://shields.io

## Idea Machine Rasberry Pi

This code is on a Raspberry Pi. The Raspberry Pi functions as an MQTT broker, which receives data from the smart cubes (see here:). The blue LEDs indicate whether each cube has established a connection to the broker. These turn on and remain on as soon as the cube has established a connection to the Pi. The sides of the dice are assigned to specific terms that are stored on the Pi. These can be customised to suit your needs. Now you have to press the buzzer until the green LED flashes. This transfers the terms to an LLM, which generates a futuristic text from them and prints it out via a thermal printer.

### Required hardware:

Raspberry Pi (Raspberry Pi 5 4 GB)  
 A thermal POS printer (58 mm)  
 A Wi-Fi interface such as a router  
 Internet  
 Microcontroller with Wi-Fi  
 MPU sensor  
 Power bank

## Installation

1. establish connection with PI

2. Clone the repository:

```bash
git clone https://github.com/technologiestiftung/idea-machine-raspi-wiesbaden.git
cd idea-machine-raspi-wiesbaden
```

3. Run setup:

```bash
chmod +x setup.sh
./setup.sh
```

4. Adjust environment variables
5. Replace example logo in "assets/logo.png"
4. unplug the printer and plug it back in

The script automatically installs:

- Mosquitto MQTT Broker
- CUPS & printer configuration
- Python venv with all dependencies
- `.env` with broker IP

6. for testing start the app locally with:
```bash
python main.py
```

## Printer

How to get the most out of the printer. For example, to create a LOGO on the bong, the LOGO must be saved as a PNG file. The font must also be completely black and the background transparent.

Follow these steps to find out the printer specifications and insert them into the code.

## Contributors

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https:/github.com/LuiseBrandenburger"><img src="https://avatars.githubusercontent.com/u/61413319?s=?s=64" width="64px;" alt="Luise Brandenburger"/><br /><sub><b>Luise Brandenburger</b></sub></a><br /><a href="https://github.com/technologiestiftung/idea-machine-raspi-wiesbaden/commits?author=LuiseBrandenburger" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Content Licensing

Texts and content available as [CC BY](https://creativecommons.org/licenses/by/3.0/de/).

Illustrations by {MARIA_MUSTERFRAU}, all rights reserved.

## Credits

<table>
  <tr>
    <td>
      Made by  <a href="https://www.technologiestiftung-berlin.de/">
        <br />
        <br />
        <img width="150" src="https://logos.citylab-berlin.org/logo-technologiestiftung-berlin-de.svg" />
      </a>
    </td>
    <td>
      Supported by <a href="https://www.berlin.de/">
        <br />
        <br />
        <img width="150" src="https://logos.citylab-berlin.org/logo-berlin.svg" />
      </a>
    </td>
  </tr>
</table>
