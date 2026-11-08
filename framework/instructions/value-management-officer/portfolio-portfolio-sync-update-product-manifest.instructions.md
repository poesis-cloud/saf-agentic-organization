---
name: portfolio-portfolio-sync-update-product-manifest
---

<!-- Copyright 2026 Poesis Cloud and contributors

     Licensed under the Apache License, Version 2.0 (the "License");
     you may not use this file except in compliance with the License.
     You may obtain a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

     Unless required by applicable law or agreed to in writing, software
     distributed under the License is distributed on an "AS IS" BASIS,
     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
     See the License for the specific language governing permissions and
     limitations under the License. -->

# Portfolio Sync — update Product Manifest

The Value Management Officer refreshes the product registry entry of the **one** product this sync names (`portfolio/products/<product-slug>/product-manifest.yaml`). Another product is another Portfolio Sync run.

Inputs: the Portfolio Manifest just updated, and that product's current state.
Output: the product-manifest artifact. Do not rewrite Product Vision or Features.
