<template>
  <Layout class="bg-gray-50 dark:bg-gray-950">
    <Preheader>First Te Moana Mahana Newsletter</Preheader>

    <Container class="max-w-xl p-0 py-10 sm:p-6">
      <Section class="rounded-t-lg bg-blue-950 px-6 pt-6 pb-11">
        <Row>
          <Column class="text-center">
            <Link href="https://te-moana-mahana.org/">
              <Img src="https://raw.githubusercontent.com/TeMoanaMahana/website/main/newsletter/2026/public/logo.png" width="120" alt="Te Moana Mahana" />
            </Link>
          </Column>
        </Row>

        <Spacer class="h-12" />

        <Heading class="mb-4 text-[32px]/10 font-bold text-white">
          2026 Te Moana Mahana Annual Newsletter
        </Heading>
        <Text class="mb-6 text-base text-white">
          Welcome to the first annual newsletter for the Te Moana Mahana Project
        </Text>
      </Section>

      <Section class="rounded-b-lg bg-white px-6 py-16 dark:bg-gray-800">

        <Markdown wrapper class="text-base text-gray-600 dark:text-gray-300">
          # Kia ora koutou!

          Thanks for signing up to the Te Moana Mahana email list!

          We’ve just completed the first year of our programme and progress has been excellent!

          We’ve made an outstanding start on all the research projects. We’ve also met with many stakeholders to discuss directions and incorporate their perspectives.

          Te Moana Mahana was created because the oceans in the New Zealand region are warming faster than the global average causing changes to weather and the coastal ocean that will challenge the resilience of our society and economy. Our programme brings together a team of oceanographers, atmospheric, and social science experts who are assessing:
          * Future coastal ocean temperatures and marine heat waves
          * Changes in extreme weather events due to the changing ocean
          * Coastal ocean thermal refugia and hot spots
          * Changes to deep ocean temperatures in our region
          * Impacts of extreme events in the coastal ocean
          * Science communication and decision-making about the ocean
        </Markdown>

        <Img src="https://raw.githubusercontent.com/TeMoanaMahana/website/main/assets/images/blog/glider-in-water.png" width="520" alt="A glider deployment" class="mb-6 rounded-lg" />

        <Markdown wrapper class="text-base text-gray-600 dark:text-gray-300">
          A highlight from the first year has been the collection of new data around the country. Two legs of the [Maui Glider Survey](https://te-moana-mahana.org/glider/) were completed to map the connection between the coastal and deep ocean along the east coast of the South Island. Te Moana Mahana also funded the [Aotearoa Marine Observing System](https://amos.org.nz/) to instrument gear on fishing vessels, which has delivered more than 6,000 temperature profiles in the coastal ocean in the first year alone. Both projects will continue to collect data over the next four years of the programme.

          Another highlight during this first year is the selection of postdoctoral researcher Gabby O’Connor as an artist in [Sculpture in the Gulf](https://www.sotg.nz/artists/gabby-oconnor) and for a [Te Whare Hēra](https://www.tewharehera.ac.nz/artists/gabby-oconnor) artist residency. These opportunities are creating a wide audience to connect with the ocean and explore its connections to the atmosphere and climate. Gabby has designed an interactive ocean experience that she will be taking to schools and community centres on Waiheke in November.
        </Markdown>

        <Img src="https://raw.githubusercontent.com/TeMoanaMahana/website/main/newsletter/2026/public/light-box.png" width="520" alt="Our team building an 'ocean', an activity done by Gabby O'Connor in schools" class="mb-6 rounded-lg" />

        <Markdown wrapper class="text-base text-gray-600 dark:text-gray-300">
          Our project to simulate extreme weather events is off to a fast start. Postdoctoral researcher Mike Kittridge has implemented weather models and tools to track moisture in our region, leading to new understanding about what parts of the ocean are the source of rainfall over the country. His results will guide us in understanding where ocean change will impact more on our precipitation and how that might change with seasons.

          Foundational work has been completed in all the projects towards the goals. The framework for the regional and coastal ocean reanalyses has been set up and implementation on subsets of data is in progress. Preparation for running climate projections of the ocean around the country are complete and set to run once the global climate simulations are released from international centres. Historic observations from our two coastal study sites, the Hauraki Gulf and Otago Shelf, are being analysed to guide the placement of new observations. Consultation, planning and pilot studies are underway for the upcoming measurement programmes. New analysis in our programme is also providing insight into how our regional ocean is changing by quantifying the subsurface oxygen trends around the country and the magnitude of a phytoplankton bloom that developed in the wake of severe Tropical Cyclone Maila earlier this year.

          Overall, it’s been a very strong foundational year, and we look forward to building on this effort as we head into the second year of Te Moana Mahana!

          All the best,

          Melissa Bowen<br>
          Programme Leader, Te Moana Mahana
        </Markdown>

        <Button
          href="https://te-moana-mahana.org"
          class="rounded-lg bg-gray-900 px-7 py-3 text-sm font-bold text-white dark:bg-white dark:text-gray-900"
        >
          Check out our website!
        </Button>

      </Section>

      <Section class="px-6 py-11 text-center">
        <Img src="https://raw.githubusercontent.com/TeMoanaMahana/website/main/newsletter/2026/public/logo-footer.png" dark-src="https://raw.githubusercontent.com/TeMoanaMahana/website/main/newsletter/2026/public/logo-footer-dark.png" width="240" alt="Te Moana Mahana" />

        <Spacer class="h-9" />

        <Text class="m-0 text-xs/4.5 text-gray-400">
          To unsubscribe from this email, please reply to this email stating you wish to unsubscribe.
        </Text>

        <Text class="m-0 text-xs/4.5 text-gray-400">
          &copy; {{ new Date().getFullYear() }} Te Moana Mahana. All rights reserved.
        </Text>
      </Section>
    </Container>
  </Layout>
</template>
